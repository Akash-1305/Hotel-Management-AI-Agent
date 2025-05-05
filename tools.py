import os
import sqlite3
from typing import List, Dict, Any, Optional, Union
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("SQLITE_DB_PATH")

def get_db_connection():
    """Create and return a database connection."""
    if not DB_PATH:
        raise ValueError("Database path not set. Please check SQLITE_DB_PATH in your .env file.")
    return sqlite3.connect(DB_PATH)

def run_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """
    Execute a SQL query with parameterized inputs and return the results.
    
    Args:
        query: SQL query with parameter placeholders
        params: Parameter values to substitute in the query
        
    Returns:
        List of dictionaries representing the query results
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        # For SELECT queries, fetch and return results
        if query.strip().lower().startswith("select") or query.strip().lower().startswith("pragma"):
            rows = cursor.fetchall()
            if cursor.description:  # Check if there are any results to process
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
            return []
        
        # For other queries, commit changes and return affected row count
        conn.commit()
        return [{"affected_rows": cursor.rowcount}]
        
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        return [{"error": f"Database error: {str(e)}"}]
    except Exception as e:
        if conn:
            conn.rollback()
        return [{"error": f"Unexpected error: {str(e)}"}]
    finally:
        if conn:
            conn.close()

def validate_table_name(table_name: str) -> bool:
    """
    Validate that a table name contains only allowed characters.
    
    Args:
        table_name: The table name to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Only allow alphanumeric characters and underscores in table names
    return table_name.isalnum() or all(c.isalnum() or c == '_' for c in table_name)

@tool
def read_records(table: str, condition: str = "", limit: int = 5) -> List[Dict[str, Any]]:
    """Read rows from a table.

    Args:
        table: Table name (e.g., 'Rooms', 'Bookings').
        condition: Optional WHERE clause (e.g., "isVacant = 1").
        limit: Max number of rows to fetch.
        
    Returns:
        List of rows as dictionaries
    """
    # Validate table name to prevent SQL injection
    if not validate_table_name(table):
        return [{"error": "Invalid table name"}]
    
    # Use parameterized query for the limit
    query = f"SELECT * FROM {table}"
    if condition:
        # Note: Conditions are still vulnerable to SQL injection
        # In a production environment, you should parse and validate conditions
        query += f" WHERE {condition}"
    
    query += " LIMIT ?"
    return run_query(query, (limit,))

@tool
def describe_table(table: str) -> List[Dict[str, Any]]:
    """Get table structure and columns.

    Args:
        table: Table name to describe.
        
    Returns:
        Table schema information
    """
    if not validate_table_name(table):
        return [{"error": "Invalid table name"}]
        
    query = "desc table " + table
    return run_query(query, (table,))

@tool
def custom_query(query: str) -> List[Dict[str, Any]]:
    """Run a custom SQL SELECT query (read-only).

    Args:
        query: A safe SELECT query to execute.
        
    Returns:
        Query results
    """
    query = query.strip()
    
    # Basic security: only allow SELECT queries
    if not query.lower().startswith("select"):
        return [{"error": "Only SELECT queries are allowed for security reasons"}]
    
    return run_query(query, ())

# Specialized hotel management tools

@tool
def get_vacant_rooms(room_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get all currently vacant rooms, optionally filtered by type.
    
    Args:
        room_type: Optional room type to filter by (e.g., '2BHK', '3BHK').
        
    Returns:
        List of vacant rooms
    """
    if room_type:
        query = "SELECT * FROM Rooms WHERE isVacant = 1 AND type = ?"
        return run_query(query, (room_type,))
    else:
        query = "SELECT * FROM Rooms WHERE isVacant = 1"
        return run_query(query, ())

@tool
def get_upcoming_arrivals(days: int = 7) -> List[Dict[str, Any]]:
    """Get bookings with upcoming arrivals within specified days.
    
    Args:
        days: Number of days to look ahead (default 7).
        
    Returns:
        List of upcoming arrivals
    """
    if not isinstance(days, int) or days < 0 or days > 365:
        return [{"error": "Days must be a positive integer less than 366"}]
        
    query = """
    SELECT b.BookingsID, b.arrivalDate, b.departureDay, 
           c.FirstName, c.LastName, r.RoomID, r.type
    FROM Bookings b
    JOIN Customers c ON b.customerID = c.CustomerID
    LEFT JOIN Rooms r ON r.currentStay = b.BookingsID
    WHERE date(b.arrivalDate) BETWEEN date('now') AND date('now', '+' || ? || ' days')
    ORDER BY b.arrivalDate
    """
    return run_query(query, (days,))

@tool
def get_upcoming_departures(days: int = 7) -> List[Dict[str, Any]]:
    """Get bookings with upcoming departures within specified days.
    
    Args:
        days: Number of days to look ahead (default 7).
        
    Returns:
        List of upcoming departures
    """
    if not isinstance(days, int) or days < 0 or days > 365:
        return [{"error": "Days must be a positive integer less than 366"}]
        
    query = """
    SELECT b.BookingsID, b.departureDay, 
           c.FirstName, c.LastName, r.RoomID, r.type
    FROM Bookings b
    JOIN Customers c ON b.customerID = c.CustomerID
    LEFT JOIN Rooms r ON r.currentStay = b.BookingsID
    WHERE date(b.departureDay) BETWEEN date('now') AND date('now', '+' || ? || ' days')
    ORDER BY b.departureDay
    """
    return run_query(query, (days,))

@tool
def get_frequent_customers(min_bookings: int = 2) -> List[Dict[str, Any]]:
    """Find customers with multiple bookings.
    
    Args:
        min_bookings: Minimum number of bookings to consider a customer frequent.
        
    Returns:
        List of frequent customers
    """
    if not isinstance(min_bookings, int) or min_bookings < 1:
        return [{"error": "Minimum bookings must be a positive integer"}]
        
    query = """
    SELECT c.CustomerID, c.FirstName, c.LastName, COUNT(b.BookingsID) as booking_count
    FROM Customers c
    JOIN Bookings b ON c.CustomerID = b.customerID
    GROUP BY c.CustomerID
    HAVING booking_count >= ?
    ORDER BY booking_count DESC
    """
    return run_query(query, (min_bookings,))

@tool
def get_room_occupancy_stats() -> List[Dict[str, Any]]:
    """Get room occupancy statistics by room type.
    
    Returns:
        Room occupancy statistics grouped by room type
    """
    query = """
    SELECT 
        type, 
        COUNT(*) as total_rooms,
        SUM(CASE WHEN isVacant = 1 THEN 1 ELSE 0 END) as vacant_rooms,
        SUM(CASE WHEN isVacant = 0 THEN 1 ELSE 0 END) as occupied_rooms,
        ROUND(SUM(CASE WHEN isVacant = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as occupancy_rate
    FROM Rooms
    GROUP BY type
    """
    return run_query(query)

@tool
def get_current_stays() -> List[Dict[str, Any]]:
    """Get all current guest stays with customer and room details.
    
    Returns:
        List of current stays with detailed information
    """
    query = """
    SELECT 
        r.RoomID, r.type, r.price,
        c.FirstName, c.LastName,
        b.arrivalDate, b.departureDay,
        p.price as booking_price, p.discount,
        p.PaymentType, p.isDone as payment_completed
    FROM Rooms r
    JOIN Bookings b ON r.currentStay = b.BookingsID
    JOIN Customers c ON b.customerID = c.CustomerID
    JOIN Pricing p ON b.paymentID = p.PaymentID
    WHERE r.isVacant = 0
    """
    return run_query(query)

@tool
def get_revenue_by_room_type(start_date: str = "", end_date: str = "") -> List[Dict[str, Any]]:
    """Get revenue statistics by room type within a date range.
    
    Args:
        start_date: Start date in format 'YYYY-MM-DD' (default: all time)
        end_date: End date in format 'YYYY-MM-DD' (default: current date)
        
    Returns:
        Revenue statistics grouped by room type
    """
    # Validate date format
    params = []
    query = """
    SELECT 
        r.type, 
        COUNT(DISTINCT b.BookingsID) as booking_count,
        SUM(p.price * (1 - p.discount/100.0)) as total_revenue,
        AVG(p.price * (1 - p.discount/100.0)) as avg_revenue_per_booking
    FROM Bookings b
    JOIN Rooms r ON r.currentStay = b.BookingsID
    JOIN Pricing p ON b.paymentID = p.PaymentID
    WHERE 1=1
    """
    
    if start_date:
        query += " AND b.arrivalDate >= ?"
        params.append(start_date)
    
    if end_date:
        query += " AND b.arrivalDate <= ?"
        params.append(end_date)
    
    query += " GROUP BY r.type"
    return run_query(query, tuple(params))

@tool
def get_customer_bookings(customer_id: int = 0, name: str = "") -> List[Dict[str, Any]]:
    """Get all bookings for a specific customer by ID or name.
    
    Args:
        customer_id: Customer ID (optional if name is provided)
        name: Customer name to search for (optional if customer_id is provided)
        
    Returns:
        List of bookings for the specified customer
    """
    if not customer_id and not name:
        return [{"error": "Either customer_id or name must be provided"}]
    
    query = """
    SELECT 
        c.CustomerID, c.FirstName, c.LastName,
        b.BookingsID, b.bookedDate, b.arrivalDate, b.departureDay,
        r.RoomID, r.type,
        p.price, p.discount, p.PaymentType, p.isDone
    FROM Customers c
    JOIN Bookings b ON c.CustomerID = b.customerID
    LEFT JOIN Rooms r ON r.currentStay = b.BookingsID
    JOIN Pricing p ON b.paymentID = p.PaymentID
    """
    
    params = []
    if customer_id:
        query += " WHERE c.CustomerID = ?"
        params.append(customer_id)
    else:
        query += " WHERE c.FirstName LIKE ? OR c.LastName LIKE ?"
        search_term = f"%{name}%"
        params.append(search_term)
        params.append(search_term)
    
    query += " ORDER BY b.arrivalDate DESC"
    return run_query(query, tuple(params))