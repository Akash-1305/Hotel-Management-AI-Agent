from langgraph.prebuilt import create_react_agent
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from tools import read_records, describe_table, custom_query
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
- Customers(CustomerID PK, DOB, IdentityType, IdentityString)
- Pricing(PaymentID PK, PaymentType, isDone, price, discount)
"""

tools = [read_records, describe_table, custom_query]

agent: Runnable = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=system_prompt
)
