import os
import sqlite3
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("SQLITE_DB_PATH")

def run_query(query: str, params: tuple = ()) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        conn.close()

@tool("read_records", parse_docstring=True)
def read_records(table: str, condition: str = "", limit: int = 5) -> list:
    """Read rows from a table.

    Args:
        table: Table name (e.g., 'Rooms', 'Bookings').
        condition: Optional WHERE clause (e.g., "isVacant = 1").
        limit: Max number of rows to fetch.
    """
    q = f"SELECT * FROM {table}"
    if condition:
        q += f" WHERE {condition}"
    q += f" LIMIT ?"
    return run_query(q, (limit,))

@tool("describe_table", parse_docstring=True)
def describe_table(table: str) -> list:
    """Get table structure and columns.

    Args:
        table: Table name to describe.
    """
    q = f"PRAGMA table_info({table});"
    return run_query(q)

@tool("custom_query", parse_docstring=True)
def custom_query(query: str) -> list:
    """Run a custom SQL SELECT query (read-only).

    Args:
        query: A safe SELECT query to execute.
    """
    if not query.strip().lower().startswith("select"):
        return [{"error": "Only SELECT queries are allowed"}]
    return run_query(query)

# Specialized hotel management tools

@tool("get_vacant_rooms", parse_docstring=True)
def get_vacant_rooms(room_type: str = "") -> list:
    """Get all currently vacant rooms, optionally filtered by type.
    
    Args:
        room_type: Optional room type to filter by (e.g., '2BHK', '3BHK').
    """
    query = "SELECT * FROM Rooms WHERE isVacant = 1"
    if room_type:
        query += f" AND type = '{room_type}'"
    return run_query(query)

@tool("get_upcoming_arrivals", parse_docstring=True)
def get_upcoming_arrivals(days: int = 7) -> list:
    """Get bookings with upcoming arrivals within specified days.
    
    Args:
        days: Number of days to look ahead (default 7).
    """
    query = f"""
    SELECT b.BookingsID, b.arrivalDate, b.departureDay, 
           c.FirstName, c.LastName, r.RoomID, r.type
    FROM Bookings b
    JOIN Customers c ON b.customerID = c.CustomerID
    LEFT JOIN Rooms r ON r.currentStay = b.BookingsID
    WHERE date(b.arrivalDate) BETWEEN date('now') AND date('now', '+{days} days')
    ORDER BY b.arrivalDate
    """
    return run_query(query)

@tool("get_upcoming_departures", parse_docstring=True)
def get_upcoming_departures(days: int = 7) -> list:
    """Get bookings with upcoming departures within specified days.
    
    Args:
        days: Number of days to look ahead (default 7).
    """
    query = f"""
    SELECT b.BookingsID, b.departureDay, 
           c.FirstName, c.LastName, r.RoomID, r.type
    FROM Bookings b
    JOIN Customers c ON b.customerID = c.CustomerID
    LEFT JOIN Rooms r ON r.currentStay = b.BookingsID
    WHERE date(b.departureDay) BETWEEN date('now') AND date('now', '+{days} days')
    ORDER BY b.departureDay
    """
    return run_query(query)

@tool("get_frequent_customers", parse_docstring=True)
def get_frequent_customers(min_bookings: int = 2) -> list:
    """Find customers with multiple bookings.
    
    Args:
        min_bookings: Minimum number of bookings to consider a customer frequent.
    """
    query = f"""
    SELECT c.CustomerID, c.FirstName, c.LastName, COUNT(b.BookingsID) as booking_count
    FROM Customers c
    JOIN Bookings b ON c.CustomerID = b.customerID
    GROUP BY c.CustomerID
    HAVING booking_count >= {min_bookings}
    ORDER BY booking_count DESC
    """
    return run_query(query)

@tool("get_room_occupancy_stats", parse_docstring=True)
def get_room_occupancy_stats() -> list:
    """Get room occupancy statistics by room type."""
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

@tool("get_current_stays", parse_docstring=True)
def get_current_stays() -> list:
    """Get all current guest stays with customer and room details."""
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

@tool("get_revenue_by_room_type", parse_docstring=True)
def get_revenue_by_room_type(start_date: str = "", end_date: str = "") -> list:
    """Get revenue statistics by room type within a date range.
    
    Args:
        start_date: Start date in format 'YYYY-MM-DD' (default: all time)
        end_date: End date in format 'YYYY-MM-DD' (default: current date)
    """
    where_clause = ""
    if start_date:
        where_clause += f" AND b.arrivalDate >= '{start_date}'"
    if end_date:
        where_clause += f" AND b.arrivalDate <= '{end_date}'"
    
    query = f"""
    SELECT 
        r.type, 
        COUNT(DISTINCT b.BookingsID) as booking_count,
        SUM(p.price * (1 - p.discount/100.0)) as total_revenue,
        AVG(p.price * (1 - p.discount/100.0)) as avg_revenue_per_booking
    FROM Bookings b
    JOIN Rooms r ON r.currentStay = b.BookingsID
    JOIN Pricing p ON b.paymentID = p.PaymentID
    WHERE 1=1 {where_clause}
    GROUP BY r.type
    """
    return run_query(query)

@tool("get_customer_bookings", parse_docstring=True)
def get_customer_bookings(customer_id: int = 0, name: str = "") -> list:
    """Get all bookings for a specific customer by ID or name.
    
    Args:
        customer_id: Customer ID (optional if name is provided)
        name: Customer name to search for (optional if customer_id is provided)
    """
    if not customer_id and not name:
        return [{"error": "Either customer_id or name must be provided"}]
    
    where_clause = ""
    if customer_id:
        where_clause = f"WHERE c.CustomerID = {customer_id}"
    elif name:
        where_clause = f"WHERE c.FirstName LIKE '%{name}%' OR c.LastName LIKE '%{name}%'"
    
    query = f"""
    SELECT 
        c.CustomerID, c.FirstName, c.LastName,
        b.BookingsID, b.bookedDate, b.arrivalDate, b.departureDay,
        r.RoomID, r.type,
        p.price, p.discount, p.PaymentType, p.isDone
    FROM Customers c
    JOIN Bookings b ON c.CustomerID = b.customerID
    LEFT JOIN Rooms r ON r.currentStay = b.BookingsID
    JOIN Pricing p ON b.paymentID = p.PaymentID
    {where_clause}
    ORDER BY b.arrivalDate DESC
    """
    return run_query(query)
