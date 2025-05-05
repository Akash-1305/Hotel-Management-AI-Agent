# Hotel Management ReAct Agent

This project is a LangChain-powered ReAct agent that interacts with a hotel management SQLite database using Google's Gemini 2.0 Flash Lite via OpenAI-compatible API. It now includes a FastAPI-based REST API for programmatic access.

## Features

- 💡 Intelligent querying using a Gemini-powered agent
- 🔍 Read table structure and query data conditionally
- 🛠️ Uses LangChain tools for modular DB interaction
- 🔒 Safe read-only queries (no insert/update/delete)
- 🗃️ SQLite backend with realistic schema and sample data
- 📊 Specialized tools for hotel analytics and insights
- 👥 Customer tracking with name and booking history
- 🚀 **NEW!** RESTful API with FastAPI for programmatic access

## Files

- `setup.py`: Creates `hotel.db` with schema and dummy data.
- `tools.py`: LangChain tools for reading records, describing tables, and running specialized hotel queries.
- `agent.py`: ReAct agent using Gemini 2.0 Flash Lite via OpenAI SDK.
- **`api.py`**: FastAPI application exposing hotel management operations as REST endpoints.
- `.env`: Required environment variables (not included in repo).
- `setup.sh`: Interactive setup script for macOS/Linux.
- `setup.bat`: Interactive setup script for Windows.

## Quick Setup (Recommended)

### For macOS/Linux Users:
```bash
chmod +x setup.sh
./setup.sh
```

### For Windows Users:
```
setup.bat
```

The interactive setup script will:
1. Check if Python is installed
2. Create and activate a virtual environment
3. Install all required dependencies
4. Guide you through creating a Google Gemini API key if you don't have one
5. Set up your `.env` file securely
6. Initialize the database with sample data
7. Let you test a query right away

## Manual Setup

If you prefer to set up manually, follow these steps:

### 1. Get a Google Gemini API Key

1. Visit the [Google AI Studio](https://aistudio.google.com/) and sign in with your Google account
2. Click on "Get API key" in the navigation menu
3. Create a new API key (or use an existing one)
4. Copy the API key - you'll need it for your `.env` file
5. **Important**: Keep your API key secure! Never commit it to version control or share it publicly

### 2. Install dependencies

```bash
pip install langchain langgraph langchain-openai python-dotenv sqlite3 fastapi uvicorn pyjwt python-multipart
```

### 3. Create a `.env` file

Create a file named `.env` in the project root directory with the following content:

```env
GEMINI_API_KEY=your_google_api_key_here
SQLITE_DB_PATH=hotel.db
JWT_SECRET_KEY=your_secret_key_here
```

Replace `your_google_api_key_here` with the actual API key you obtained and use a strong random string for `JWT_SECRET_KEY`.

**Security Warning**: Never commit your `.env` file to version control or share it with others. Add it to your `.gitignore` file.

### 4. Run the database setup

```bash
python setup.py
```

This will create the SQLite database with sample data for testing.

### 5. Query the agent

Example usage:

```python
from agent import agent
response = agent.invoke({"input": "List all vacant 2BHK rooms."})
print(response["output"])
```

## Available Specialized Tools

The system includes several specialized tools for hotel analytics:

- **Room Management**: Find vacant rooms by type
- **Guest Movement**: Track upcoming arrivals and departures
- **Customer Insights**: Identify frequent customers and booking history
- **Business Intelligence**: Analyze occupancy rates and revenue performance

## REST API Usage

The project now includes a complete REST API built with FastAPI that can be used to programmatically access and manage the hotel system.

### Starting the API Server

```bash
# Make sure your virtual environment is activated first
python api.py
```

The API server will start on http://localhost:8000. You can view the interactive API documentation at http://localhost:8000/docs.

### API Authentication

The API uses JWT token-based authentication:

1. Login using the `/api/auth/login` endpoint with username "admin" and password "password123" (demo credentials)
2. Use the returned access token in the Authorization header for other requests: `Bearer {token}`

### Available Endpoints

#### Authentication
- `POST /api/auth/login` - Obtain access token
- `POST /api/auth/logout` - Logout (invalidate token)
- `POST /api/auth/refresh-token` - Refresh access token

#### Room Management
- `GET /api/rooms` - List all rooms
- `GET /api/rooms/{room_id}` - Get room details
- `GET /api/rooms/available` - Get available rooms
- `PUT /api/rooms/{room_id}/status` - Update room status

#### Booking Management
- `GET /api/bookings` - List all bookings
- `GET /api/bookings/{booking_id}` - Get booking details
- `POST /api/bookings` - Create new booking
- `PUT /api/bookings/{booking_id}` - Update booking
- `DELETE /api/bookings/{booking_id}` - Cancel booking
- `POST /api/bookings/{booking_id}/check-in` - Check-in guest
- `POST /api/bookings/{booking_id}/check-out` - Check-out guest

#### Guest Management
- `GET /api/guests` - List all guests
- `GET /api/guests/{guest_id}` - Get guest details
- `POST /api/guests` - Create new guest
- `PUT /api/guests/{guest_id}` - Update guest information

#### Statistics & Analytics
- `GET /api/stats/occupancy` - Get current occupancy stats
- `GET /api/stats/bookings` - Get booking statistics
- `GET /api/stats/revenue` - Get revenue data
- `GET /api/stats/forecast` - Get occupancy forecast

#### AI Chat
- `POST /api/chat/message` - Send message to AI assistant
- `GET /api/chat/history` - Get chat history

### Example API Usage

Using curl to authenticate and get available rooms:

```bash
# Login and get token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/auth/login" -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin&password=password123" | jq -r '.access_token')

# Get available rooms
curl -X GET "http://localhost:8000/api/rooms/available" -H "Authorization: Bearer $TOKEN"
```

---

## Schema Overview

- `Rooms(RoomID, isVacant, currentStay, type, price)`
- `Bookings(BookingsID, customerID, bookedDate, arrivalDate, departureDay, paymentID)`
- `Customers(CustomerID, FirstName, LastName, DOB, IdentityType, IdentityString)`
- `Pricing(PaymentID, PaymentType, isDone, price, discount)`

