# tools.py

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
        # For other queries, commit changes and return useful information
        if query.strip().lower().startswith("insert"):
            last_id = cursor.lastrowid
            table_name = query.split("INTO")[1].split("(")[0].strip() if "INTO" in query else "unknown"
            id_field = f"{table_name[:-1] if table_name.endswith('s') else table_name}ID"
            return [{"success": True, "affected_rows": cursor.rowcount, id_field: last_id}]
        else:
            return [{"success": True, "affected_rows": cursor.rowcount}]
        
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
    """Get all current guest stays with customer, booking, and room details, including departure date.
    
    Returns:
        List of current stays with detailed information
    """
    query = """
    SELECT
        r.*, 
        b.BookingsID, b.arrivalDate, b.departureDay, 
        c.FirstName, c.LastName
    FROM Rooms r
    JOIN Bookings b ON r.currentStay = b.BookingsID
    JOIN Customers c ON b.customerID = c.CustomerID
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


@tool
def add_customer(first_name: str, last_name: str, dob: str, identity_type: str, identity_string: str) -> List[Dict[str, Any]]:
    """Add a new customer."""
    query = """
    INSERT INTO Customers (FirstName, LastName, DOB, IdentityType, IdentityString)
    VALUES (?, ?, ?, ?, ?)
    """
    return run_query(query, (first_name, last_name, dob, identity_type, identity_string))

@tool
def add_payment(payment_type: str, price: float, discount: float = 0.0, is_done: bool = False) -> List[Dict[str, Any]]:
    """Add a new payment record."""
    query = """
    INSERT INTO Pricing (PaymentType, isDone, price, discount)
    VALUES (?, ?, ?, ?)
    """
    return run_query(query, (payment_type, int(is_done), price, discount))

@tool
def book_room(customer_id: int, room_id: int, arrival_date: str, departure_day: str, payment_id: int) -> List[Dict[str, Any]]:
    """Book a room and update room status."""
    booking_query = """
    INSERT INTO Bookings (customerID, bookedDate, arrivalDate, departureDay, paymentID, RoomID)
    VALUES (?, date('now'), ?, ?, ?, ?)
    """
    result = run_query(booking_query, (customer_id, arrival_date, departure_day, payment_id, room_id))
    if "error" in result[0]:
        return result
    booking_id = result[0].get("BookingID", None)
    return [{"booking_id": booking_id}]

@tool
def check_in_guest(room_id: int, booking_id: int) -> List[Dict[str, Any]]:
    """Manually check in a guest by updating room status, ensuring the room is vacant and booking matches the room and is valid for today."""
    # Check if the room is vacant
    room_status = run_query("SELECT isVacant, currentStay FROM Rooms WHERE RoomID = ?", (room_id,))
    if not room_status:
        return [{"error": "Room not found"}]
    if room_status[0].get("isVacant") == 0:
        return [{"error": "Room is already occupied"}]

    # Check if the booking exists and is not assigned to another room
    booking = run_query("SELECT BookingsID, arrivalDate, departureDay, RoomID FROM Bookings WHERE BookingsID = ?", (booking_id,))
    if not booking:
        return [{"error": "Booking not found"}]

    # Check if the booking is already assigned to another room
    assigned_room = run_query("SELECT RoomID FROM Rooms WHERE currentStay = ?", (booking_id,))
    if assigned_room:
        return [{"error": "Booking is already assigned to another room (RoomID: %s)" % assigned_room[0].get("RoomID") }]

    # Check if today's date is within the booking's arrival and departure dates
    arrival = booking[0]["arrivalDate"]
    departure = booking[0]["departureDay"]
    today_query = "SELECT date('now') as today"
    today_result = run_query(today_query)
    today = today_result[0]["today"] if today_result else None
    if not (arrival <= today <= departure):
        return [{"error": f"Booking is not valid for today (today: {today}, arrival: {arrival}, departure: {departure})"}]

    # All checks passed, perform check-in
    update_room = run_query("UPDATE Rooms SET isVacant = 0, currentStay = ? WHERE RoomID = ?", (booking_id, room_id))
    update_booking = run_query("UPDATE Bookings SET RoomID = ? WHERE BookingsID = ?", (room_id, booking_id))
    return [{"room_update": update_room[0], "booking_update": update_booking[0]}]

@tool
def checkout_guest(room_id: int) -> List[Dict[str, Any]]:
    """Check out a guest by marking room as vacant and clearing currentStay."""
    query = "UPDATE Rooms SET isVacant = 1, currentStay = NULL WHERE RoomID = ?"
    return run_query(query, (room_id,))

@tool
def update_customer_info(customer_id: int, first_name: Optional[str] = None,
                         last_name: Optional[str] = None, dob: Optional[str] = None,
                         identity_type: Optional[str] = None, identity_string: Optional[str] = None) -> List[Dict[str, Any]]:
    """Update customer details selectively."""
    fields = []
    values = []
    if first_name:
        fields.append("FirstName = ?")
        values.append(first_name)
    if last_name:
        fields.append("LastName = ?")
        values.append(last_name)
    if dob:
        fields.append("DOB = ?")
        values.append(dob)
    if identity_type:
        fields.append("IdentityType = ?")
        values.append(identity_type)
    if identity_string:
        fields.append("IdentityString = ?")
        values.append(identity_string)

    if not fields:
        return [{"error": "No fields provided to update"}]

    query = f"UPDATE Customers SET {', '.join(fields)} WHERE CustomerID = ?"
    values.append(customer_id)
    return run_query(query, tuple(values))

@tool
def cancel_booking(booking_id: int) -> List[Dict[str, Any]]:
    """Cancel a booking and free the room."""
    free_room_query = "UPDATE Rooms SET isVacant = 1, currentStay = NULL WHERE currentStay = ?"
    result1 = run_query(free_room_query, (booking_id,))

    delete_booking_query = "DELETE FROM Bookings WHERE BookingsID = ?"
    result2 = run_query(delete_booking_query, (booking_id,))

    return [{"freed_room_rows": result1[0].get("affected_rows", 0),
             "deleted_booking_rows": result2[0].get("affected_rows", 0)}]

@tool
def apply_discount(payment_id: int, discount: float) -> List[Dict[str, Any]]:
    """Apply or update a discount for a payment record."""
    if discount < 0 or discount > 100:
        return [{"error": "Discount must be between 0 and 100"}]

    query = "UPDATE Pricing SET discount = ? WHERE PaymentID = ?"
    return run_query(query, (discount, payment_id))

# NEW TOOLS

@tool
def get_room_by_id(room_id: int) -> List[Dict[str, Any]]:
    """Get detailed information about a specific room by its ID.
    
    Args:
        room_id: The ID of the room to retrieve
        
    Returns:
        Detailed information about the specified room
    """
    query = """
    SELECT r.*,
           b.BookingsID, b.arrivalDate, b.departureDay,
           c.FirstName, c.LastName
    FROM Rooms r
    LEFT JOIN Bookings b ON r.currentStay = b.BookingsID
    LEFT JOIN Customers c ON b.customerID = c.CustomerID
    WHERE r.RoomID = ?
    """
    return run_query(query, (room_id,))

@tool
def get_customer_by_id(customer_id: int) -> List[Dict[str, Any]]:
    """Get detailed information about a specific customer by their ID.
    
    Args:
        customer_id: The ID of the customer to retrieve
        
    Returns:
        Detailed information about the specified customer
    """
    query = """
    SELECT c.*,
           COUNT(b.BookingsID) as total_bookings,
           MAX(b.arrivalDate) as last_stay
    FROM Customers c
    LEFT JOIN Bookings b ON c.CustomerID = b.customerID
    WHERE c.CustomerID = ?
    GROUP BY c.CustomerID
    """
    return run_query(query, (customer_id,))

@tool
def get_booking_details(booking_id: int) -> List[Dict[str, Any]]:
    """Get detailed information about a specific booking by its ID.
    
    Args:
        booking_id: The ID of the booking to retrieve
        
    Returns:
        Detailed information about the specified booking
    """
    query = """
    SELECT 
        b.*,
        c.FirstName, c.LastName, c.IdentityType, c.IdentityString,
        r.RoomID, r.type as room_type, r.price as room_price,
        p.PaymentType, p.price as payment_amount, p.discount, p.isDone as payment_completed,
        JULIANDAY(b.departureDay) - JULIANDAY(b.arrivalDate) as stay_duration,
        p.price * (1 - p.discount/100.0) as final_amount
    FROM Bookings b
    JOIN Customers c ON b.customerID = c.CustomerID
    LEFT JOIN Rooms r ON r.currentStay = b.BookingsID
    JOIN Pricing p ON b.paymentID = p.PaymentID
    WHERE b.BookingsID = ?
    """
    return run_query(query, (booking_id,))

@tool
def search_rooms_by_price(min_price: float = 0, max_price: float = 10000, only_vacant: bool = False) -> List[Dict[str, Any]]:
    """Search for rooms within a specific price range.
    
    Args:
        min_price: Minimum room price (default: 0)
        max_price: Maximum room price (default: 10000)
        only_vacant: Whether to only include vacant rooms
        
    Returns:
        List of rooms that match the specified criteria
    """
    query = """
    SELECT * FROM Rooms 
    WHERE price BETWEEN ? AND ?
    """
    params = [min_price, max_price]
    
    if only_vacant:
        query += " AND isVacant = 1"
    
    query += " ORDER BY price ASC"
    return run_query(query, tuple(params))

@tool
def get_room_availability(room_id: int, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """Check if a specific room is available during a date range.
    
    Args:
        room_id: The ID of the room to check
        start_date: Start date in format 'YYYY-MM-DD'
        end_date: End date in format 'YYYY-MM-DD'
        
    Returns:
        Availability information for the specified room and date range
    """
    query = """
    SELECT 
        r.RoomID, r.type, r.price, r.isVacant,
        CASE 
            WHEN r.isVacant = 0 AND r.currentStay IS NOT NULL THEN 'Currently occupied'
            WHEN COUNT(b.BookingsID) > 0 THEN 'Has bookings in specified period'
            ELSE 'Available for the entire period' 
        END as availability_status,
        GROUP_CONCAT(b.arrivalDate || ' to ' || b.departureDay) as conflicting_bookings
    FROM Rooms r
    LEFT JOIN Bookings b ON 
        b.BookingsID IN (
            SELECT b2.BookingsID FROM Bookings b2
            LEFT JOIN Rooms r2 ON r2.currentStay = b2.BookingsID
            WHERE r2.RoomID = ? AND (
                (b2.arrivalDate <= ? AND b2.departureDay >= ?) OR
                (b2.arrivalDate >= ? AND b2.arrivalDate <= ?)
            )
        )
    WHERE r.RoomID = ?
    GROUP BY r.RoomID
    """
    params = (room_id, end_date, start_date, start_date, end_date, room_id)
    return run_query(query, params)

@tool
def list_bookings_by_date_range(start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """List all bookings within a specific date range.
    
    Args:
        start_date: Start date in format 'YYYY-MM-DD'
        end_date: End date in format 'YYYY-MM-DD'
        
    Returns:
        List of bookings within the specified date range
    """
    query = """
    SELECT 
        b.BookingsID, b.arrivalDate, b.departureDay,
        c.FirstName, c.LastName,
        r.RoomID, r.type as room_type,
        p.price, p.discount, p.PaymentType, p.isDone as payment_completed,
        JULIANDAY(b.departureDay) - JULIANDAY(b.arrivalDate) as stay_duration
    FROM Bookings b
    JOIN Customers c ON b.customerID = c.CustomerID
    LEFT JOIN Rooms r ON r.currentStay = b.BookingsID
    JOIN Pricing p ON b.paymentID = p.PaymentID
    WHERE 
        (b.arrivalDate BETWEEN ? AND ?) OR
        (b.departureDay BETWEEN ? AND ?) OR
        (b.arrivalDate <= ? AND b.departureDay >= ?)
    ORDER BY b.arrivalDate
    """
    params = (start_date, end_date, start_date, end_date, start_date, end_date)
    return run_query(query, params)

@tool
def get_payment_details(payment_id: int) -> List[Dict[str, Any]]:
    """Get detailed information about a payment.
    
    Args:
        payment_id: The ID of the payment to retrieve
        
    Returns:
        Detailed information about the specified payment
    """
    query = """
    SELECT 
        p.*,
        p.price * (1 - p.discount/100.0) as final_amount,
        b.BookingsID, b.arrivalDate, b.departureDay,
        c.FirstName, c.LastName,
        r.RoomID, r.type as room_type
    FROM Pricing p
    LEFT JOIN Bookings b ON p.PaymentID = b.paymentID
    LEFT JOIN Customers c ON b.customerID = c.CustomerID
    LEFT JOIN Rooms r ON r.currentStay = b.BookingsID
    WHERE p.PaymentID = ?
    """
    return run_query(query, (payment_id,))

@tool
def update_room_info(room_id: int, is_vacant: Optional[bool] = None, 
                    room_type: Optional[str] = None, price: Optional[float] = None) -> List[Dict[str, Any]]:
    """Update room information.
    
    Args:
        room_id: ID of the room to update
        is_vacant: Whether the room is vacant
        room_type: Type of the room ('2BHK' or '3BHK')
        price: Price of the room per night
        
    Returns:
        Result of the update operation
    """
    fields = []
    values = []
    
    if is_vacant is not None:
        fields.append("isVacant = ?")
        values.append(int(is_vacant))
    
    if room_type is not None:
        if room_type not in ('2BHK', '3BHK'):
            return [{"error": "Room type must be either '2BHK' or '3BHK'"}]
        fields.append("type = ?")
        values.append(room_type)
    
    if price is not None:
        if price <= 0:
            return [{"error": "Price must be greater than zero"}]
        fields.append("price = ?")
        values.append(price)
    
    if not fields:
        return [{"error": "No fields provided to update"}]
    
    query = f"UPDATE Rooms SET {', '.join(fields)} WHERE RoomID = ?"
    values.append(room_id)
    
    return run_query(query, tuple(values))

@tool
def update_booking_details(booking_id: int, arrival_date: Optional[str] = None, 
                          departure_day: Optional[str] = None, payment_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Update booking details.
    
    Args:
        booking_id: ID of the booking to update
        arrival_date: New arrival date in format 'YYYY-MM-DD'
        departure_day: New departure date in format 'YYYY-MM-DD'
        payment_id: New payment ID
        
    Returns:
        Result of the update operation
    """
    fields = []
    values = []
    
    if arrival_date is not None:
        fields.append("arrivalDate = ?")
        values.append(arrival_date)
    
    if departure_day is not None:
        fields.append("departureDay = ?")
        values.append(departure_day)
    
    if payment_id is not None:
        fields.append("paymentID = ?")
        values.append(payment_id)
    
    if not fields:
        return [{"error": "No fields provided to update"}]
    
    query = f"UPDATE Bookings SET {', '.join(fields)} WHERE BookingsID = ?"
    values.append(booking_id)
    
    return run_query(query, tuple(values))

@tool
def get_hotel_statistics() -> List[Dict[str, Any]]:
    """Generate comprehensive hotel statistics including occupancy, revenue, and booking trends.
    
    Returns:
        Statistical overview of hotel performance
    """
    queries = [
        # Overall occupancy
        """
        SELECT 
            COUNT(*) as total_rooms,
            SUM(CASE WHEN isVacant = 1 THEN 1 ELSE 0 END) as vacant_rooms,
            SUM(CASE WHEN isVacant = 0 THEN 1 ELSE 0 END) as occupied_rooms,
            ROUND(SUM(CASE WHEN isVacant = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as occupancy_rate
        FROM Rooms
        """,
        
        # Revenue statistics
        """
        SELECT 
            SUM(p.price * (1 - p.discount/100.0)) as total_revenue,
            AVG(p.price * (1 - p.discount/100.0)) as avg_revenue_per_booking,
            SUM(CASE WHEN p.isDone = 1 THEN p.price * (1 - p.discount/100.0) ELSE 0 END) as realized_revenue,
            SUM(CASE WHEN p.isDone = 0 THEN p.price * (1 - p.discount/100.0) ELSE 0 END) as pending_revenue
        FROM Pricing p
        JOIN Bookings b ON p.PaymentID = b.paymentID
        """,
        
        # Booking statistics
        """
        SELECT 
            COUNT(*) as total_bookings,
            COUNT(DISTINCT customerID) as unique_customers,
            AVG(JULIANDAY(departureDay) - JULIANDAY(arrivalDate)) as avg_stay_duration,
            (SELECT COUNT(*) FROM Bookings WHERE date(arrivalDate) >= date('now')) as upcoming_bookings,
            (SELECT COUNT(*) FROM Bookings 
             JOIN Rooms ON Rooms.currentStay = Bookings.BookingsID
             WHERE Rooms.isVacant = 0) as active_bookings
        FROM Bookings
        """,
        
        # Room type popularity
        """
        SELECT 
            r.type, 
            COUNT(b.BookingsID) as booking_count,
            ROUND(COUNT(b.BookingsID) * 100.0 / (SELECT COUNT(*) FROM Bookings), 2) as booking_percentage
        FROM Rooms r
        JOIN Bookings b ON r.currentStay = b.BookingsID OR 
                          (r.RoomID IN (SELECT RoomID FROM Rooms WHERE currentStay = b.BookingsID))
        GROUP BY r.type
        """
    ]
    
    results = {}
    for i, query in enumerate(queries):
        result = run_query(query)
        if result and not "error" in result[0]:
            category = ["occupancy", "revenue", "bookings", "popularity"][i]
            results[category] = result[0]
    
    return [results]

@tool
def add_new_room(room_id: int, room_type: str, price: float) -> List[Dict[str, Any]]:
    """Add a new room to the hotel inventory.
    
    Args:
        room_id: Unique ID for the new room
        room_type: Type of room ('2BHK' or '3BHK')
        price: Price per night for the room
        
    Returns:
        Result of the room addition operation
    """
    if room_type not in ('2BHK', '3BHK'):
        return [{"error": "Room type must be either '2BHK' or '3BHK'"}]
    
    if price <= 0:
        return [{"error": "Price must be greater than zero"}]
    
    query = """
    INSERT INTO Rooms (RoomID, isVacant, type, price)
    VALUES (?, 1, ?, ?)
    """
    
    return run_query(query, (room_id, room_type, price))

@tool
def search_customers(search_term: str) -> List[Dict[str, Any]]:
    """Search for customers by name, ID type, or ID string.
    
    Args:
        search_term: Term to search for in customer records
        
    Returns:
        List of customers matching the search criteria
    """
    query = """
    SELECT 
        c.*,
        COUNT(b.BookingsID) as booking_count,
        MAX(b.arrivalDate) as last_stay
    FROM Customers c
    LEFT JOIN Bookings b ON c.CustomerID = b.customerID
    WHERE 
        c.FirstName LIKE ? OR
        c.LastName LIKE ? OR
        c.IdentityString LIKE ?
    GROUP BY c.CustomerID
    ORDER BY c.LastName, c.FirstName
    """
    
    search_pattern = f"%{search_term}%"
    params = (search_pattern, search_pattern, search_pattern)
    
    return run_query(query, params)

@tool
def get_all_tables() -> List[Dict[str, Any]]:
    """Get a list of all tables in the hotel database.
    
    Returns:
        List of all database tables
    """
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    return run_query(query)

@tool
def get_all_customers() -> List[Dict[str, Any]]:
    """Retrieve all customers from the database.
    
    Returns:
        List of all customers
    """
    query = "SELECT * FROM Customers"
    return run_query(query)

@tool
def get_all_bookings() -> List[Dict[str, Any]]:
    """Retrieve all bookings from the database, including associated room information.
    
    Returns:
        List of all bookings with room details
    """
    query = """
    SELECT 
        b.*, 
        r.RoomID, r.type as room_type, r.price as room_price
    FROM Bookings b
    LEFT JOIN Rooms r ON r.RoomID = b.RoomID
    """
    return run_query(query)

@tool
def get_all_rooms() -> List[Dict[str, Any]]:
    """Retrieve all rooms from the database.
    
    Returns:
        List of all rooms
    """
    query = "SELECT * FROM Rooms"
    return run_query(query)

@tool
def get_all_payments() -> List[Dict[str, Any]]:
    """Retrieve all payments from the database.

    Returns:
        List of all payments
    """
    query = "SELECT * FROM Pricing"
    return run_query(query)