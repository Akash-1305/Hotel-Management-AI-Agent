from fastapi import FastAPI, HTTPException, Query, Path, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import sqlite3
import os
from dotenv import load_dotenv

# Import tools from tools.py
from tools import (
    read_records, 
    describe_table, 
    custom_query,
    get_vacant_rooms,
    get_upcoming_arrivals,
    get_upcoming_departures,
    get_frequent_customers,
    get_room_occupancy_stats,
    get_current_stays,
    get_revenue_by_room_type,
    get_customer_bookings,
    run_query
)

load_dotenv()
DB_PATH = os.getenv("SQLITE_DB_PATH")

app = FastAPI(title="Hotel Management API", 
             description="API for hotel management system operations",
             version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class Room(BaseModel):
    RoomID: int
    isVacant: bool
    currentStay: Optional[int] = None
    type: str
    price: float

class RoomUpdate(BaseModel):
    isVacant: Optional[bool] = None
    currentStay: Optional[int] = None
    
class Booking(BaseModel):
    BookingsID: Optional[int] = None
    customerID: int
    bookedDate: str
    arrivalDate: str
    departureDay: str
    paymentID: int

class BookingCreate(BaseModel):
    customerID: int
    arrivalDate: str
    departureDay: str
    roomType: str
    paymentType: str
    price: float
    discount: float = 0

class Customer(BaseModel):
    CustomerID: Optional[int] = None
    FirstName: str
    LastName: str
    DOB: str
    IdentityType: str
    IdentityString: str

class ChatMessage(BaseModel):
    message: str
    
class AIResponse(BaseModel):
    response: str

# Utility functions for database operations
def execute_write_query(query: str, params: tuple = ()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return {"success": True, "last_row_id": cursor.lastrowid}
    except Exception as e:
        conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        conn.close()

# Room Management Endpoints
@app.get("/api/rooms", response_model=List[Dict[str, Any]])
async def list_rooms(
    limit: int = Query(50, description="Maximum number of rooms to retrieve")
):
    return read_records(table="Rooms", limit=limit)

@app.get("/api/rooms/{room_id}", response_model=Dict[str, Any])
async def get_room_details(
    room_id: int = Path(..., description="The ID of the room to retrieve")
):
    results = read_records(table="Rooms", condition=f"RoomID = {room_id}", limit=1)
    if not results:
        raise HTTPException(status_code=404, detail="Room not found")
    return results[0]

@app.get("/api/rooms/available", response_model=List[Dict[str, Any]])
async def get_available_rooms(
    room_type: str = Query(None, description="Filter by room type")
):
    return get_vacant_rooms(room_type=room_type if room_type else "")

@app.put("/api/rooms/{room_id}/status", response_model=Dict[str, Any])
async def update_room_status(
    room_id: int = Path(..., description="The ID of the room to update"),
    room_update: RoomUpdate = Body(...)
):
    # Build the SET clause for the SQL query based on provided fields
    set_parts = []
    params = []
    
    if room_update.isVacant is not None:
        set_parts.append("isVacant = ?")
        params.append(1 if room_update.isVacant else 0)
        
    if room_update.currentStay is not None:
        set_parts.append("currentStay = ?")
        params.append(room_update.currentStay)
        
    if not set_parts:
        raise HTTPException(status_code=400, detail="No fields to update provided")
    
    set_clause = ", ".join(set_parts)
    query = f"UPDATE Rooms SET {set_clause} WHERE RoomID = ?"
    params.append(room_id)
    
    result = execute_write_query(query, tuple(params))
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    
    # Return updated room details
    updated_room = read_records(table="Rooms", condition=f"RoomID = {room_id}", limit=1)
    if not updated_room:
        raise HTTPException(status_code=404, detail="Room not found after update")
    return updated_room[0]

# Booking Management Endpoints
@app.get("/api/bookings", response_model=List[Dict[str, Any]])
async def list_bookings(
    limit: int = Query(50, description="Maximum number of bookings to retrieve")
):
    return read_records(table="Bookings", limit=limit)

@app.get("/api/bookings/{booking_id}", response_model=Dict[str, Any])
async def get_booking_details(
    booking_id: int = Path(..., description="The ID of the booking to retrieve")
):
    query = f"""
    SELECT 
        b.*, 
        c.FirstName, c.LastName, 
        r.RoomID, r.type as room_type,
        p.price, p.discount, p.PaymentType, p.isDone as payment_completed
    FROM Bookings b
    JOIN Customers c ON b.customerID = c.CustomerID
    LEFT JOIN Rooms r ON r.currentStay = b.BookingsID
    JOIN Pricing p ON b.paymentID = p.PaymentID
    WHERE b.BookingsID = {booking_id}
    """
    results = custom_query(query)
    if not results or "error" in results[0]:
        raise HTTPException(status_code=404, detail="Booking not found")
    return results[0]

@app.post("/api/bookings", response_model=Dict[str, Any])
async def create_booking(
    booking: BookingCreate = Body(...)
):
    # 1. Create payment record first
    payment_query = """
    INSERT INTO Pricing (PaymentType, isDone, price, discount) 
    VALUES (?, ?, ?, ?)
    """
    payment_params = (booking.paymentType, 0, booking.price, booking.discount)
    payment_result = execute_write_query(payment_query, payment_params)
    
    if not payment_result["success"]:
        raise HTTPException(status_code=500, detail=f"Failed to create payment: {payment_result['error']}")
    
    payment_id = payment_result["last_row_id"]
    
    # 2. Create booking record
    booking_query = """
    INSERT INTO Bookings (customerID, bookedDate, arrivalDate, departureDay, paymentID) 
    VALUES (?, date('now'), ?, ?, ?)
    """
    booking_params = (booking.customerID, booking.arrivalDate, booking.departureDay, payment_id)
    booking_result = execute_write_query(booking_query, booking_params)
    
    if not booking_result["success"]:
        # Rollback payment if booking creation fails
        execute_write_query("DELETE FROM Pricing WHERE PaymentID = ?", (payment_id,))
        raise HTTPException(status_code=500, detail=f"Failed to create booking: {booking_result['error']}")
    
    booking_id = booking_result["last_row_id"]
    
    # 3. Find a vacant room of the requested type
    vacant_rooms = get_vacant_rooms(room_type=booking.roomType)
    if not vacant_rooms:
        # Rollback both records if no suitable room is found
        execute_write_query("DELETE FROM Bookings WHERE BookingsID = ?", (booking_id,))
        execute_write_query("DELETE FROM Pricing WHERE PaymentID = ?", (payment_id,))
        raise HTTPException(status_code=400, detail=f"No vacant rooms of type {booking.roomType} available")
    
    room_id = vacant_rooms[0]["RoomID"]
    
    # 4. Mark the room as occupied
    room_update_query = "UPDATE Rooms SET isVacant = 0, currentStay = ? WHERE RoomID = ?"
    room_update_result = execute_write_query(room_update_query, (booking_id, room_id))
    
    if not room_update_result["success"]:
        # Rollback both records if room update fails
        execute_write_query("DELETE FROM Bookings WHERE BookingsID = ?", (booking_id,))
        execute_write_query("DELETE FROM Pricing WHERE PaymentID = ?", (payment_id,))
        raise HTTPException(status_code=500, detail=f"Failed to update room: {room_update_result['error']}")
    
    # Return the created booking with details
    return get_booking_details(booking_id=booking_id)

@app.put("/api/bookings/{booking_id}", response_model=Dict[str, Any])
async def update_booking(
    booking_id: int = Path(..., description="The ID of the booking to update"),
    booking_data: Dict[str, Any] = Body(...)
):
    # Check if booking exists
    existing_booking = read_records(table="Bookings", condition=f"BookingsID = {booking_id}", limit=1)
    if not existing_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Build SQL update query
    allowed_fields = ["arrivalDate", "departureDay"]
    set_parts = []
    params = []
    
    for field in allowed_fields:
        if field in booking_data:
            set_parts.append(f"{field} = ?")
            params.append(booking_data[field])
    
    if not set_parts:
        raise HTTPException(status_code=400, detail="No valid fields to update provided")
    
    set_clause = ", ".join(set_parts)
    query = f"UPDATE Bookings SET {set_clause} WHERE BookingsID = ?"
    params.append(booking_id)
    
    result = execute_write_query(query, tuple(params))
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    
    # Return updated booking
    return get_booking_details(booking_id=booking_id)

@app.delete("/api/bookings/{booking_id}", response_model=Dict[str, Any])
async def cancel_booking(
    booking_id: int = Path(..., description="The ID of the booking to cancel")
):
    # Get booking details first to get associated room and payment
    booking_query = """
    SELECT b.*, r.RoomID 
    FROM Bookings b
    LEFT JOIN Rooms r ON r.currentStay = b.BookingsID
    WHERE b.BookingsID = ?
    """
    booking_result = run_query(booking_query, (booking_id,))
    
    if not booking_result:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking_data = booking_result[0]
    payment_id = booking_data.get("paymentID")
    room_id = booking_data.get("RoomID")
    
    # 1. Free up the room if it's occupied by this booking
    if room_id:
        room_query = "UPDATE Rooms SET isVacant = 1, currentStay = NULL WHERE RoomID = ? AND currentStay = ?"
        room_result = execute_write_query(room_query, (room_id, booking_id))
        if not room_result["success"]:
            raise HTTPException(status_code=500, detail=f"Failed to update room: {room_result['error']}")
    
    # 2. Delete the booking
    booking_delete_query = "DELETE FROM Bookings WHERE BookingsID = ?"
    booking_result = execute_write_query(booking_delete_query, (booking_id,))
    if not booking_result["success"]:
        raise HTTPException(status_code=500, detail=f"Failed to delete booking: {booking_result['error']}")
    
    # 3. Delete associated payment record
    if payment_id:
        payment_query = "DELETE FROM Pricing WHERE PaymentID = ?"
        execute_write_query(payment_query, (payment_id,))
    
    return {"detail": "Booking successfully cancelled", "booking_id": booking_id}

@app.post("/api/bookings/{booking_id}/check-in", response_model=Dict[str, Any])
async def check_in_guest(
    booking_id: int = Path(..., description="The ID of the booking for check-in")
):
    # Verify booking exists and get room details
    booking_query = """
    SELECT b.*, r.RoomID 
    FROM Bookings b
    LEFT JOIN Rooms r ON r.currentStay = b.BookingsID
    WHERE b.BookingsID = ?
    """
    booking_result = run_query(booking_query, (booking_id,))
    
    if not booking_result:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking_data = booking_result[0]
    room_id = booking_data.get("RoomID")
    
    # If room is not already assigned, find a vacant room
    if not room_id:
        # Find a vacant room (ideally of the right type)
        vacant_rooms = get_vacant_rooms()
        if not vacant_rooms:
            raise HTTPException(status_code=400, detail="No vacant rooms available for check-in")
        
        room_id = vacant_rooms[0]["RoomID"]
        
        # Assign room to this booking
        room_update_query = "UPDATE Rooms SET isVacant = 0, currentStay = ? WHERE RoomID = ?"
        room_result = execute_write_query(room_update_query, (booking_id, room_id))
        
        if not room_result["success"]:
            raise HTTPException(status_code=500, detail=f"Failed to assign room: {room_result['error']}")
    
    # Update booking status if needed (in a real app, you might have a status field)
    
    return {
        "detail": "Guest successfully checked in",
        "booking_id": booking_id,
        "room_id": room_id
    }

@app.post("/api/bookings/{booking_id}/check-out", response_model=Dict[str, Any])
async def check_out_guest(
    booking_id: int = Path(..., description="The ID of the booking for check-out"),
    mark_payment_complete: bool = Query(True, description="Whether to mark payment as complete")
):
    # Get booking and room details
    booking_query = """
    SELECT b.*, r.RoomID, p.PaymentID 
    FROM Bookings b
    LEFT JOIN Rooms r ON r.currentStay = b.BookingsID
    JOIN Pricing p ON b.paymentID = p.PaymentID
    WHERE b.BookingsID = ?
    """
    booking_result = run_query(booking_query, (booking_id,))
    
    if not booking_result:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking_data = booking_result[0]
    room_id = booking_data.get("RoomID")
    payment_id = booking_data.get("PaymentID")
    
    # 1. Free up the room
    if room_id:
        room_query = "UPDATE Rooms SET isVacant = 1, currentStay = NULL WHERE RoomID = ?"
        room_result = execute_write_query(room_query, (room_id,))
        if not room_result["success"]:
            raise HTTPException(status_code=500, detail=f"Failed to free up room: {room_result['error']}")
    
    # 2. Mark payment as complete if requested
    if mark_payment_complete and payment_id:
        payment_query = "UPDATE Pricing SET isDone = 1 WHERE PaymentID = ?"
        payment_result = execute_write_query(payment_query, (payment_id,))
        if not payment_result["success"]:
            raise HTTPException(status_code=500, detail=f"Failed to update payment: {payment_result['error']}")
    
    return {
        "detail": "Guest successfully checked out",
        "booking_id": booking_id,
        "room_id": room_id,
        "payment_completed": mark_payment_complete
    }

# Guest Management Endpoints
@app.get("/api/guests", response_model=List[Dict[str, Any]])
async def list_guests(
    limit: int = Query(50, description="Maximum number of guests to retrieve")
):
    return read_records(table="Customers", limit=limit)

@app.get("/api/guests/{guest_id}", response_model=Dict[str, Any])
async def get_guest_details(
    guest_id: int = Path(..., description="The ID of the guest to retrieve")
):
    results = read_records(table="Customers", condition=f"CustomerID = {guest_id}", limit=1)
    if not results:
        raise HTTPException(status_code=404, detail="Guest not found")
    return results[0]

@app.post("/api/guests", response_model=Dict[str, Any])
async def create_guest(
    guest: Customer = Body(...)
):
    query = """
    INSERT INTO Customers (FirstName, LastName, DOB, IdentityType, IdentityString) 
    VALUES (?, ?, ?, ?, ?)
    """
    params = (guest.FirstName, guest.LastName, guest.DOB, guest.IdentityType, guest.IdentityString)
    
    result = execute_write_query(query, params)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    
    guest_id = result["last_row_id"]
    created_guest = read_records(table="Customers", condition=f"CustomerID = {guest_id}", limit=1)
    
    if not created_guest:
        raise HTTPException(status_code=404, detail="Failed to retrieve created guest")
    
    return created_guest[0]

@app.put("/api/guests/{guest_id}", response_model=Dict[str, Any])
async def update_guest(
    guest_id: int = Path(..., description="The ID of the guest to update"),
    guest_data: Dict[str, Any] = Body(...)
):
    # Check if guest exists
    existing_guest = read_records(table="Customers", condition=f"CustomerID = {guest_id}", limit=1)
    if not existing_guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    
    # Build SQL update query
    allowed_fields = ["FirstName", "LastName", "DOB", "IdentityType", "IdentityString"]
    set_parts = []
    params = []
    
    for field in allowed_fields:
        if field in guest_data:
            set_parts.append(f"{field} = ?")
            params.append(guest_data[field])
    
    if not set_parts:
        raise HTTPException(status_code=400, detail="No valid fields to update provided")
    
    set_clause = ", ".join(set_parts)
    query = f"UPDATE Customers SET {set_clause} WHERE CustomerID = ?"
    params.append(guest_id)
    
    result = execute_write_query(query, tuple(params))
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    
    # Return updated guest
    updated_guest = read_records(table="Customers", condition=f"CustomerID = {guest_id}", limit=1)
    if not updated_guest:
        raise HTTPException(status_code=404, detail="Guest not found after update")
    
    return updated_guest[0]

# Statistics & Analytics Endpoints
@app.get("/api/stats/occupancy", response_model=List[Dict[str, Any]])
async def get_occupancy_stats():
    return get_room_occupancy_stats()

@app.get("/api/stats/bookings", response_model=Dict[str, Any])
async def get_booking_statistics(
    start_date: str = Query(None, description="Start date in format YYYY-MM-DD"),
    end_date: str = Query(None, description="End date in format YYYY-MM-DD")
):
    # Get booking counts by date
    date_filter = ""
    if start_date:
        date_filter += f" AND bookedDate >= '{start_date}'"
    if end_date:
        date_filter += f" AND bookedDate <= '{end_date}'"
    
    bookings_by_date_query = f"""
    SELECT 
        date(bookedDate) as booking_date, 
        COUNT(*) as booking_count
    FROM Bookings
    WHERE 1=1 {date_filter}
    GROUP BY date(bookedDate)
    ORDER BY booking_date
    """
    
    bookings_by_date = custom_query(bookings_by_date_query)
    
    # Get total bookings, average stay length
    overall_stats_query = f"""
    SELECT 
        COUNT(*) as total_bookings,
        AVG(julianday(departureDay) - julianday(arrivalDate)) as avg_stay_length,
        MIN(julianday(departureDay) - julianday(arrivalDate)) as min_stay_length,
        MAX(julianday(departureDay) - julianday(arrivalDate)) as max_stay_length
    FROM Bookings
    WHERE 1=1 {date_filter}
    """
    
    overall_stats = custom_query(overall_stats_query)
    
    return {
        "bookings_by_date": bookings_by_date,
        "overall_stats": overall_stats[0] if overall_stats else {}
    }

@app.get("/api/stats/revenue", response_model=Dict[str, Any])
async def get_revenue_data(
    start_date: str = Query(None, description="Start date in format YYYY-MM-DD"),
    end_date: str = Query(None, description="End date in format YYYY-MM-DD")
):
    # Get revenue by room type
    revenue_by_room = get_revenue_by_room_type(
        start_date=start_date if start_date else "",
        end_date=end_date if end_date else ""
    )
    
    # Get revenue by date
    date_filter = ""
    if start_date:
        date_filter += f" AND b.arrivalDate >= '{start_date}'"
    if end_date:
        date_filter += f" AND b.arrivalDate <= '{end_date}'"
    
    revenue_by_date_query = f"""
    SELECT 
        date(b.arrivalDate) as arrival_date,
        SUM(p.price * (1 - p.discount/100.0)) as daily_revenue
    FROM Bookings b
    JOIN Pricing p ON b.paymentID = p.PaymentID
    WHERE 1=1 {date_filter}
    GROUP BY date(b.arrivalDate)
    ORDER BY arrival_date
    """
    
    revenue_by_date = custom_query(revenue_by_date_query)
    
    # Get overall revenue stats
    overall_revenue_query = f"""
    SELECT 
        SUM(p.price * (1 - p.discount/100.0)) as total_revenue,
        AVG(p.price * (1 - p.discount/100.0)) as avg_revenue_per_booking,
        COUNT(CASE WHEN p.isDone = 1 THEN 1 END) as completed_payments,
        COUNT(CASE WHEN p.isDone = 0 THEN 1 END) as pending_payments
    FROM Bookings b
    JOIN Pricing p ON b.paymentID = p.PaymentID
    WHERE 1=1 {date_filter}
    """
    
    overall_revenue = custom_query(overall_revenue_query)
    
    return {
        "revenue_by_room_type": revenue_by_room,
        "revenue_by_date": revenue_by_date,
        "overall_revenue": overall_revenue[0] if overall_revenue else {}
    }

@app.get("/api/stats/forecast", response_model=Dict[str, Any])
async def get_occupancy_forecast(
    days: int = Query(30, description="Number of days to forecast")
):
    # Get total rooms count
    rooms_query = "SELECT COUNT(*) as total_rooms FROM Rooms"
    rooms_result = custom_query(rooms_query)
    total_rooms = rooms_result[0]['total_rooms'] if rooms_result else 0
    
    # Get upcoming arrivals and departures for forecast calculation
    forecast_query = f"""
    WITH dates(date) AS (
        SELECT date('now')
        UNION ALL
        SELECT date(date, '+1 day')
        FROM dates
        WHERE date < date('now', '+{days} day')
    ),
    arrivals AS (
        SELECT date(arrivalDate) as date, COUNT(*) as arrival_count
        FROM Bookings
        WHERE date(arrivalDate) BETWEEN date('now') AND date('now', '+{days} day')
        GROUP BY date(arrivalDate)
    ),
    departures AS (
        SELECT date(departureDay) as date, COUNT(*) as departure_count
        FROM Bookings
        WHERE date(departureDay) BETWEEN date('now') AND date('now', '+{days} day')
        GROUP BY date(departureDay)
    ),
    current_occupancy AS (
        SELECT COUNT(*) as occupied_rooms FROM Rooms WHERE isVacant = 0
    )
    SELECT 
        dates.date,
        IFNULL(arrivals.arrival_count, 0) as arrivals,
        IFNULL(departures.departure_count, 0) as departures,
        (SELECT occupied_rooms FROM current_occupancy) + 
        SUM(IFNULL(arrivals.arrival_count, 0) - IFNULL(departures.departure_count, 0)) 
        OVER (ORDER BY dates.date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as projected_occupancy,
        ROUND(((SELECT occupied_rooms FROM current_occupancy) + 
        SUM(IFNULL(arrivals.arrival_count, 0) - IFNULL(departures.departure_count, 0)) 
        OVER (ORDER BY dates.date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)) * 100.0 / {total_rooms}, 2) as occupancy_rate
    FROM dates
    LEFT JOIN arrivals ON dates.date = arrivals.date
    LEFT JOIN departures ON dates.date = departures.date
    ORDER BY dates.date
    """
    
    forecast_data = custom_query(forecast_query)
    
    return {
        "total_rooms": total_rooms,
        "forecast_data": forecast_data
    }

# AI Chat endpoints
@app.post("/api/chat/message", response_model=AIResponse)
async def send_chat_message(
    message: ChatMessage = Body(...)
):
    # In a real implementation, you would call your LLM-based assistant here
    # For now, we're just returning a mock response
    
    query = message.message.lower()
    response = "I don't have an answer for that query."
    
    if "vacant" in query or "available" in query:
        rooms = get_vacant_rooms()
        room_count = len(rooms)
        response = f"There are currently {room_count} vacant rooms available."
        if room_count > 0:
            room_types = set(room["type"] for room in rooms)
            response += f" Room types available: {', '.join(room_types)}."
    
    elif "arrivals" in query or "arriving" in query:
        days = 7  # Default
        if "today" in query:
            days = 1
        arrivals = get_upcoming_arrivals(days)
        response = f"There are {len(arrivals)} guests arriving in the next {days} days."
    
    elif "departures" in query or "leaving" in query or "check out" in query:
        days = 7  # Default
        if "today" in query:
            days = 1
        departures = get_upcoming_departures(days)
        response = f"There are {len(departures)} guests checking out in the next {days} days."
    
    elif "occupancy" in query or "occupancy rate" in query:
        stats = get_room_occupancy_stats()
        if stats:
            overall = sum(stat["occupied_rooms"] for stat in stats) / sum(stat["total_rooms"] for stat in stats) * 100
            response = f"Current overall occupancy rate is {overall:.2f}%."
            for stat in stats:
                response += f"\n{stat['type']}: {stat['occupancy_rate']}% ({stat['occupied_rooms']}/{stat['total_rooms']} rooms occupied)"
    
    return {"response": response}

@app.get("/api/chat/history", response_model=List[Dict[str, Any]])
async def get_chat_history():
    # In a real implementation, you would fetch chat history from a database
    # For this demo, we return a mock response
    return [
        {"timestamp": "2025-05-05T10:00:00", "user": "admin", "message": "What's our occupancy rate today?"},
        {"timestamp": "2025-05-05T10:00:05", "system": True, "message": "Current overall occupancy rate is 78.50%."}
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)