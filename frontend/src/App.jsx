import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/layout/Layout";
import Dashboard from "./components/dashboard/Dashboard";
import Reservations from "./components/Reservation/Reservations";
import Rooms from "./components/Rooms/Rooms";
import Customers from "./components/Customers/Customers";
import NewBookingForm from "./components/Reservation/NewBookingForm";
import "bootstrap/dist/css/bootstrap.min.css";

export const API_BASE = "http://127.0.0.1:8000";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="/reservations" element={<Reservations />} />
          <Route path="/rooms" element={<Rooms />} />
          <Route path="/newBooking" element={<NewBookingForm />} />
          <Route path="/customers" element={<Customers />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
