from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
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
    get_customer_bookings
)
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    model="gemini-2.0-flash-lite",
    temperature=0
)

system_prompt = """
You are a hotel management assistant. You interact with a SQLite database to answer questions about rooms, bookings, customers, and pricing.

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
    get_customer_bookings
]

agent: Runnable = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=system_prompt
)
