# Hotel Management ReAct Agent

This project is a LangChain-powered ReAct agent that interacts with a hotel management SQLite database using Google's Gemini 2.0 Flash Lite via OpenAI-compatible API.

## Features

- 💡 Intelligent querying using a Gemini-powered agent
- 🔍 Read table structure and query data conditionally
- 🛠️ Uses LangChain tools for modular DB interaction
- 🔒 Safe read-only queries (no insert/update/delete)
- 🗃️ SQLite backend with realistic schema and sample data

## Files

- `setup.py`: Creates `hotel.db` with schema and dummy data.
- `tools.py`: LangChain tools for reading records, describing tables, and running SELECT queries.
- `agent.py`: ReAct agent using Gemini 2.0 Flash Lite via OpenAI SDK.
- `.env`: Required environment variables (not included in repo).

## Setup

### 1. Install dependencies

```bash
pip install langchain langgraph langchain-openai python-dotenv
```

### 2. Create a `.env` file

```env
GEMINI_API_KEY=your_google_api_key
SQLITE_DB_PATH=hotel.db
```

### 3. Run the database setup

```bash
python setup.py
```

### 4. Query the agent

Example usage:

```python
from agent import agent
response = agent.invoke({"input": "List all vacant 2BHK rooms."})
print(response["output"])
```

---

## Schema Overview

- `Rooms(RoomID, isVacant, currentStay, type, price)`
- `Bookings(BookingsID, customerID, bookedDate, arrivalDate, departureDay, paymentID)`
- `Customers(CustomerID, DOB, IdentityType, IdentityString)`
- `Pricing(PaymentID, PaymentType, isDone, price, discount)`

