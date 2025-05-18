from fastapi import FastAPI, Query
from typing import Optional
from tools import (
    get_vacant_rooms, get_upcoming_arrivals, get_upcoming_departures,
    get_frequent_customers, get_room_occupancy_stats, get_current_stays,
    get_revenue_by_room_type, get_customer_bookings, add_customer,
    add_payment, book_room, check_in_guest, checkout_guest,
    update_customer_info, cancel_booking, apply_discount,
    get_room_by_id, get_customer_by_id, get_booking_details,
    search_rooms_by_price, get_room_availability, list_bookings_by_date_range,
    get_payment_details, update_room_info, update_booking_details,
    get_hotel_statistics, add_new_room, search_customers, get_all_tables,
    get_all_customers, get_all_bookings, get_all_rooms, get_all_payments
)
from langchain_core.messages import HumanMessage
from agent import agent, parse_ai_and_tools_messages
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/vacant-rooms")
def vacant_rooms(room_type: Optional[str] = None):
    return get_vacant_rooms.run({"room_type": room_type})

@app.get("/arrivals")
def arrivals(days: int = 7):
    return get_upcoming_arrivals.run({"days": days})

@app.get("/departures")
def departures(days: int = 7):
    return get_upcoming_departures.run({"days": days})

@app.get("/frequent-customers")
def frequent_customers(min_bookings: int = 2):
    return get_frequent_customers.run({"min_bookings": min_bookings})

@app.get("/occupancy-stats")
def occupancy_stats():
    return get_room_occupancy_stats.run({})

@app.get("/current-stays")
def current_stays():
    return get_current_stays.run({})

@app.get("/revenue")
def revenue(start_date: str = "", end_date: str = ""):
    return get_revenue_by_room_type.run({"start_date": start_date, "end_date": end_date})

@app.get("/customer-bookings")
def customer_bookings(customer_id: int = 0, name: str = ""):
    return get_customer_bookings.run({"customer_id": customer_id, "name": name})

@app.post("/add-customer")
def add_new_customer(first_name: str, last_name: str, dob: str, identity_type: str, identity_string: str):
    return add_customer.run({
        "first_name": first_name, "last_name": last_name,
        "dob": dob, "identity_type": identity_type, "identity_string": identity_string
    })

@app.post("/add-payment")
def new_payment(payment_type: str, price: float, discount: float = 0.0, is_done: bool = False):
    return add_payment.run({
        "payment_type": payment_type, "price": price,
        "discount": discount, "is_done": is_done
    })

@app.post("/book-room")
def book_room_api(customer_id: int, room_id: int, arrival_date: str, departure_day: str, payment_id: int):
    return book_room.run({
        "customer_id": customer_id, "room_id": room_id,
        "arrival_date": arrival_date, "departure_day": departure_day,
        "payment_id": payment_id
    })

@app.post("/check-in")
def check_in(room_id: int, booking_id: int):
    return check_in_guest.run({"room_id": room_id, "booking_id": booking_id})

@app.post("/check-out")
def check_out(room_id: int):
    return checkout_guest.run({"room_id": room_id})

@app.put("/update-customer")
def update_customer(
    customer_id: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    dob: Optional[str] = None,
    identity_type: Optional[str] = None,
    identity_string: Optional[str] = None
):
    return update_customer_info.run({
        "customer_id": customer_id,
        "first_name": first_name, "last_name": last_name,
        "dob": dob, "identity_type": identity_type,
        "identity_string": identity_string
    })

@app.delete("/cancel-booking")
def cancel(booking_id: int):
    return cancel_booking.run({"booking_id": booking_id})

@app.put("/apply-discount")
def apply(payment_id: int, discount: float):
    return apply_discount.run({"payment_id": payment_id, "discount": discount})

# New API endpoints

@app.get("/room/{room_id}")
def get_room(room_id: int):
    """Get detailed information about a specific room by ID"""
    return get_room_by_id.run({"room_id": room_id})

@app.get("/customer/{customer_id}")
def get_customer(customer_id: int):
    """Get detailed information about a specific customer by ID"""
    return get_customer_by_id.run({"customer_id": customer_id})

@app.get("/booking/{booking_id}")
def get_booking(booking_id: int):
    """Get detailed information about a specific booking by ID"""
    return get_booking_details.run({"booking_id": booking_id})

@app.get("/rooms/search")
def search_rooms(min_price: float = 0, max_price: float = 10000, only_vacant: bool = False):
    """Search for rooms within a specific price range"""
    return search_rooms_by_price.run({
        "min_price": min_price,
        "max_price": max_price,
        "only_vacant": only_vacant
    })

@app.get("/room-availability/{room_id}")
def room_availability(room_id: int, start_date: str, end_date: str):
    """Check if a specific room is available during a date range"""
    return get_room_availability.run({
        "room_id": room_id,
        "start_date": start_date,
        "end_date": end_date
    })

@app.get("/bookings/date-range")
def bookings_by_date(start_date: str, end_date: str):
    """List all bookings within a specific date range"""
    return list_bookings_by_date_range.run({
        "start_date": start_date,
        "end_date": end_date
    })

@app.get("/payment/{payment_id}")
def payment_details(payment_id: int):
    """Get detailed information about a payment"""
    return get_payment_details.run({"payment_id": payment_id})

@app.put("/update-room/{room_id}")
def update_room(
    room_id: int,
    is_vacant: Optional[bool] = None,
    room_type: Optional[str] = None,
    price: Optional[float] = None
):
    """Update room information"""
    return update_room_info.run({
        "room_id": room_id,
        "is_vacant": is_vacant,
        "room_type": room_type,
        "price": price
    })

@app.put("/update-booking/{booking_id}")
def update_booking(
    booking_id: int,
    arrival_date: Optional[str] = None,
    departure_day: Optional[str] = None,
    payment_id: Optional[int] = None
):
    """Update booking details"""
    return update_booking_details.run({
        "booking_id": booking_id,
        "arrival_date": arrival_date,
        "departure_day": departure_day,
        "payment_id": payment_id
    })

@app.get("/hotel-statistics")
def hotel_statistics():
    """Generate comprehensive hotel statistics"""
    return get_hotel_statistics.run({})

@app.post("/add-room")
def add_room(room_id: int, room_type: str, price: float):
    """Add a new room to the hotel inventory"""
    return add_new_room.run({
        "room_id": room_id,
        "room_type": room_type,
        "price": price
    })

@app.get("/customers/search")
def find_customers(search_term: str):
    """Search for customers by name, ID type, or ID string"""
    return search_customers.run({"search_term": search_term})

@app.get("/tables")
def all_tables():
    """Get a list of all tables in the database"""
    return get_all_tables.run({})

@app.get("/all-customers")
def all_customers():
    """Retrieve all customers from the database"""
    return get_all_customers.run({})

@app.get("/all-bookings")
def all_bookings():
    """Retrieve all bookings from the database"""
    return get_all_bookings.run({})

@app.get("/all-rooms")
def all_rooms():
    """Retrieve all rooms from the database"""
    return get_all_rooms.run({})

@app.get("/all-payments")
def all_payments():
    """Retrieve all payments from the database"""
    return get_all_payments.run({})

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("frontend/index.html", "r", encoding="utf-8") as file:
        return file.read()
    
@app.get("/chat-ai")
async def serve_chat_ai(user_query:str):
    resAi = await agent.ainvoke({"messages": [
            HumanMessage(content=user_query),]})
    print(resAi)
    resAi = parse_ai_and_tools_messages(resAi["messages"])
    return resAi

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)