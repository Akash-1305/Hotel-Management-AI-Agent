# Hotel Management ReAct Agent – Project Report

## 1. Introduction
This project implements an intelligent hotel management assistant using a ReAct agent architecture powered by Google Gemini 2.0 Flash Lite (via OpenAI-compatible API) and LangChain/LangGraph. The system interacts with a realistic hotel management SQLite database, providing both a conversational AI interface and a RESTful API for programmatic access.

## 2. System Architecture

### 2.1 Core Components
- **agent.py**: Orchestrates the AI agent, configures the LLM, system prompt, and registers all database tools.
- **tools.py**: Implements all business logic and database access as modular, reusable tools.
- **api.py**: Exposes the agent and database operations as a FastAPI REST API.
- **hotel.db**: SQLite database storing all hotel data.

### 2.2 Data Flow
1. User sends a query (via chat or API).
2. The agent interprets the query, selects appropriate tools from `tools.py`.
3. Tools execute SQL queries on `hotel.db` and return results.
4. The agent formats and returns the response to the user.

## 3. Database Schema

### 3.1 Table Structure
- **Rooms**
  - `RoomID` (Primary Key)
  - `isVacant` (Boolean)
  - `currentStay` (Foreign Key → Bookings.BookingsID)
  - `type` (e.g., '2BHK', '3BHK')
  - `price` (Numeric)

- **Bookings**
  - `BookingsID` (Primary Key)
  - `customerID` (Foreign Key → Customers.CustomerID)
  - `bookedDate` (Date)
  - `arrivalDate` (Date)
  - `departureDay` (Date)
  - `paymentID` (Foreign Key → Pricing.PaymentID)
  - `RoomID` (Foreign Key → Rooms.RoomID)

- **Customers**
  - `CustomerID` (Primary Key)
  - `FirstName`
  - `LastName`
  - `DOB` (Date of Birth)
  - `IdentityType` (e.g., passport, ID card)
  - `IdentityString` (ID number)

- **Pricing**
  - `PaymentID` (Primary Key)
  - `PaymentType` (e.g., credit card, cash)
  - `isDone` (Boolean)
  - `price` (Numeric)
  - `discount` (Numeric or percentage)

### 3.2 Relationships
- Bookings link customers, rooms, and payments.
- Rooms reference current bookings.
- Payments are associated with bookings.

## 4. Agent and Tooling Design

### 4.1 Agent (agent.py)
- Loads environment variables and configures the Gemini LLM.
- Defines a detailed system prompt, including behavioral rules and available tools.
- Registers all tools from `tools.py`.
- Uses `create_react_agent` for orchestrating tool use and conversation.
- Provides a message parsing utility for formatting responses.

### 4.2 Tools (tools.py) – In Depth

All business logic and database access is encapsulated in tools, each implemented as a Python function decorated with `@tool`. These tools are the only way the agent can interact with the database, ensuring security and modularity.

#### 4.2.1 General Utilities
- **Database Connection**: Securely loads the database path from environment variables and provides a connection utility.
- **Query Execution**: All SQL is executed via a safe, parameterized function (`run_query`).
- **Table Name Validation**: Prevents SQL injection by validating table names.

#### 4.2.2 Data Access Tools
- `read_records`: Read rows from any table with optional filtering and limit.
- `describe_table`: Get schema/column info for a table.
- `custom_query`: Run arbitrary SELECT queries (read-only, with security checks).
- `get_all_tables`, `get_all_customers`, `get_all_bookings`, `get_all_rooms`, `get_all_payments`: List all entries in respective tables.

#### 4.2.3 Room Management Tools
- `get_vacant_rooms`: List vacant rooms, optionally filtered by type.
- `get_room_by_id`: Get detailed info for a specific room.
- `search_rooms_by_price`: Find rooms within a price range.
- `get_room_availability`: Check if a room is available for a date range.
- `add_new_room`: Add a new room to inventory.
- `update_room_info`: Update room type, price, or vacancy status.

#### 4.2.4 Booking Management Tools
- `get_upcoming_arrivals`, `get_upcoming_departures`: Track guest movement.
- `get_customer_bookings`: List all bookings for a customer.
- `book_room`: Book a room for a customer and update status.
- `cancel_booking`: Cancel a booking and free the room.
- `list_bookings_by_date_range`: List bookings within a date range.
- `get_booking_details`: Get comprehensive booking info.
- `update_booking_details`: Change booking dates or payment info.

#### 4.2.5 Customer Management Tools
- `get_frequent_customers`: Identify customers with multiple bookings.
- `add_customer`: Add a new customer.
- `update_customer_info`: Update customer details.
- `get_customer_by_id`: Get detailed info for a customer.
- `search_customers`: Search by name or ID info.

#### 4.2.6 Payment & Pricing Tools
- `add_payment`: Create a new payment record.
- `apply_discount`: Apply/update a discount for a payment.
- `get_payment_details`: View payment info.

#### 4.2.7 Analytics & Statistics Tools
- `get_room_occupancy_stats`: Occupancy by room type.
- `get_revenue_by_room_type`: Revenue analysis by room type and date range.
- `get_hotel_statistics`: Comprehensive hotel performance stats.
- `get_current_stays`: View all current guests with room and payment details.

#### 4.2.8 Check-in/Check-out Tools
- `check_in_guest`: Mark a room as occupied for a booking.
- `checkout_guest`: Mark a room as vacant and clear assignment.

### 4.3 Security and Best Practices
- All SQL queries are parameterized to prevent injection.
- Only SELECT queries are allowed in `custom_query`.
- Table names are validated.
- All database access is funneled through tools, ensuring auditability and control.

## 5. REST API (api.py)
- Built with FastAPI, exposes endpoints for all major operations (room, booking, guest, statistics, chat).
- Uses JWT authentication for secure access.
- Integrates with the agent for AI-powered chat and analytics.

## 6. Extensibility
- New tools can be added to `tools.py` and registered in `agent.py` to expand system capabilities.
- The modular design allows for easy adaptation to other domains or database schemas.

## 7. Example Use Cases
- List all vacant rooms of a certain type.
- Find frequent customers and their booking history.
- Analyze revenue by room type for a given period.
- Check if a room is available for a specific date range.
- Add a new customer and book a room for them.
- Apply a discount to a payment and view updated revenue stats.

## 8. Conclusion
This project demonstrates a robust, modular, and secure approach to building an AI-powered hotel management system. By leveraging LangChain, Gemini LLM, and a well-structured toolset, it provides both conversational and programmatic interfaces for efficient hotel operations and analytics.

---

*For further details, see the code in `agent.py`, `tools.py`, and `api.py`.*

