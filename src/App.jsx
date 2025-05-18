import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/layout/Layout";
import Dashboard from "./pages/Dashboard";
import Reservations from "./pages/Reservations";
import Rooms from "./pages/Rooms";
import Reports from "./pages/Reports";
import NewBookingForm from "./pages/NewBookingForm";

export const API_BASE = "http://127.0.0.1:8000";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="/reservations" element={<Reservations />} />
          <Route path="/rooms" element={<Rooms />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/NewBooking" element={<NewBookingForm />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
