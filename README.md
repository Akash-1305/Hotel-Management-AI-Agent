# Hotel Management

A **Hotel Management** built with **FastAPI (backend)** and **React Vite (frontend)**, with AI-powered chat support via **LangChain Agent**.  
This application allows hotel staff to manage rooms, bookings, customers, payments, and generate statistics with ease.

---

## Features

### Backend (FastAPI)

- **Room Management**

  - Add, update, search, and check availability of rooms
  - View occupancy statistics

- **Customer Management**

  - Add, update, and search customers
  - Get frequent customers
  - Retrieve all customers

- **Booking Management**

  - Book rooms, cancel bookings, check-in & check-out guests
  - Update booking details
  - List bookings by date range

- **Hotel Insights**

  - Revenue by room type
  - Current stays & upcoming arrivals/departures
  - Hotel-wide statistics

- **Database Access**

  - Fetch all customers, rooms, bookings, and tables

- **AI-Powered Chat**
  - `/chat-ai` endpoint with **LangChain agent** to handle natural language queries

---

### Frontend (React + Vite)

- Built with **React Vite**
- Provides:
  - Interactive dashboards
  - Room & booking management
  - Customer search and insights
  - AI chatbot integration

---

## Tech Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)
- **Frontend:** [React](https://react.dev/) + [Vite](https://vitejs.dev/)
- **AI Agent:** [LangChain](https://www.langchain.com/) + custom tools
- **Database:** (Any SQL DB, e.g., PostgreSQL / MySQL / SQLite)
- **Others:** CORS Middleware, RESTful APIs

---

## Setup Instructions

### Clone Repository

```bash
git clone https://github.com/Akash-1305/hotel-management-system.git
cd hotel-management-system
```

### Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
# On Windows
venv\Scripts\Activate.ps1
# On macOS/Linux
source venv/bin/Activate.ps1
```

Installation required Python packages:

```bash
.\setup.bat
```

Run the backend:

```bash
python api.py
```

Backend will be live at **http://127.0.0.1:8000**

API Docs: **http://127.0.0.1:8000/docs**

---

### Frontend Setup (React Vite)

```bash
cd frontend
npm install
npm run dev
```

Frontend will be live at **http://127.0.0.1:5173**

---

## AI Chat Assistant

- Ask natural queries like:
  - _“Show me all vacant rooms”_
  - _“List customers with more than 3 bookings”_
  - _“Get revenue report for August”_

The agent will parse queries and call backend tools automatically.

---

## Future Improvements

- Authentication & role-based access
- Integration with payment gateways
- Advanced analytics dashboards
- Notifications & email confirmations

---

## Contributions

Contributions are welcome! Please fork the repository and create a pull request.

---

## Issues & Support

If you encounter any issues, please check the GitHub Issues section for existing solutions or report a new issue.

For further assistance, feel free to reach out via email: akash20050513@gmail.com & mohamedkamran2211@gmail.com.

We appreciate feedback and suggestions to improve the platform!

---

### Acknowledgments

Thanks to the creators of React, Vite, Tailwind, Python, and FastAPI for making this project possible!
