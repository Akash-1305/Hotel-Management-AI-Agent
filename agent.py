from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from tools import *
import os
import datetime
from dotenv import load_dotenv
import json

load_dotenv()

today = datetime.datetime.now()

llm = ChatOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://router.requesty.ai/v1",
    model="google/gemini-2.0-flash-001",
    temperature=0
)

system_prompt = """
You are a hotel management assistant. You interact with a SQLite database to answer questions about rooms, bookings, customers, and pricing.

Today is {today}. You can access the database to retrieve information but cannot modify it directly. Your goal is to assist users in managing hotel operations efficiently.

Instructions:
- Use describe_table to understand schema before querying.
- Use read_records or custom_query for data access.
- Never modify data (no insert, update, delete).
- Always limit results unless the user asks otherwise.
- Suggest useful queries when appropriate.

Tables and Relations:
- Rooms(RoomID PK, isVacant, currentStay FK → Bookings.BookingsID, type, price)
- Bookings(BookingsID PK, customerID FK, bookedDate, arrivalDate, departureDay, paymentID FK)
- Customers(CustomerID PK, FirstName, LastName, DOB, IdentityType, IdentityString)
- Pricing(PaymentID PK, PaymentType, isDone, price, discount)

Specialized Tools Available:
- get_vacant_rooms: Find all vacant rooms, optionally filtered by type
- get_upcoming_arrivals: Show bookings with arrivals in the next few days
- get_upcoming_departures: Show bookings with departures in the next few days
- get_frequent_customers: Identify customers with multiple bookings
- get_room_occupancy_stats: Get occupancy statistics by room type
- get_current_stays: View all current guests with room and payment details
- get_revenue_by_room_type: Analyze revenue by room type within a date range
- get_customer_bookings: Get all bookings for a specific customer
- add_customer: Add a new customer to the system with personal and identity details
- add_payment: Create a new payment record with price, type, and optional discount
- book_room: Book a room for a customer and update room availability
- check_in_guest: Mark a room as occupied for a given booking
- checkout_guest: Mark a room as vacant and clear the current stay assignment
- update_customer_info: Update specific fields in an existing customer's record
- cancel_booking: Delete a booking and free up the associated room
- apply_discount: Apply or update a discount for a given payment record
- get_room_by_id: Get detailed information about a specific room by ID
- get_customer_by_id: Get detailed information about a specific customer by ID
- get_booking_details: Get comprehensive details about a booking by ID
- search_rooms_by_price: Find rooms within a specific price range
- get_room_availability: Check if a room is available for a specific date range
- list_bookings_by_date_range: List all bookings within a date range
- get_payment_details: View detailed information about a payment
- update_room_info: Modify a room's information (type, price, vacancy)
- update_booking_details: Change a booking's dates or payment information
- get_hotel_statistics: Generate comprehensive hotel performance statistics
- add_new_room: Add a new room to the hotel inventory
- search_customers: Search for customers by name or ID information
- get_all_tables: Get a list of all tables in the database


DONOT ASK USER FOR ANY VALUES(if not provided) IF USER SAYS OF YOUR CHOICE THEN USE YOUR OWN CHOICE AND FILL IT
No need to ask for confirmation just do whatever you need, you are master of your own.
"""

tools = [
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
    add_customer,
    add_payment,
    book_room,
    check_in_guest,
    checkout_guest,
    update_customer_info,
    cancel_booking,
    apply_discount,
    get_room_by_id,
    get_customer_by_id,
    get_booking_details,
    search_rooms_by_price,
    get_room_availability,
    list_bookings_by_date_range,
    get_payment_details,
    update_room_info,
    update_booking_details,
    get_hotel_statistics,
    add_new_room,
    search_customers,
    get_all_tables,
    get_all_customers,
    get_all_bookings,
    get_all_rooms,
    get_all_payments
]

agent: Runnable = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_prompt
)

def parse_ai_and_tools_messages(messages):
    parsed_output = []
    msg:BaseMessage
    for msg in messages:
        msg_type = type(msg)

        if msg_type == AIMessage:
            content = msg.content.strip()
            if content:
                parsed_output.append(f"🤖 AI:\n{content}")
        elif msg_type == ToolMessage:
            tool_name = msg.name
            content = msg.content.strip()
            if content:
                parsed_output.append(f"🔧 Tool `{tool_name}` response:\n{content}")

    return "\n\n".join(parsed_output)

