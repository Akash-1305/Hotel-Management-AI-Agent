import React, { useState, useEffect } from "react";
import axios from "axios";
import { API_BASE } from "../../App";

const NewBookingForm = ({ onClose }) => {
  const [formData, setFormData] = useState({
    customer_id: "",
    room_id: "",
    arrival_date: "",
    departure_day: "",
    payment_id: "",
  });

  const [customers, setCustomers] = useState([]);
  const [rooms, setRooms] = useState([]);

  const getTodayDate = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  useEffect(() => {
    getAllRooms();
    getUsers();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const today = getTodayDate();

    if (formData.arrival_date < today) {
      alert("Arrival date cannot be earlier than today.");
      return;
    }

    if (formData.departure_day < formData.arrival_date) {
      alert("Departure date must be after arrival date.");
      return;
    }

    try {
      await axios.post(`${API_BASE}/book-room`, null, {
        params: {
          customer_id: parseInt(formData.customer_id),
          room_id: parseInt(formData.room_id),
          arrival_date: formData.arrival_date,
          departure_day: formData.departure_day,
          payment_id: parseInt(formData.payment_id),
        },
      });

      alert("Room booked successfully!");

      setFormData({
        customer_id: "",
        room_id: "",
        arrival_date: "",
        departure_day: "",
        payment_id: "",
      });

      if (onClose) onClose();
    } catch (err) {
      console.error("Booking error:", err);
      alert("Error during booking. Check console.");
    }
  };

  const getAllRooms = () => {
    axios
      .get(`${API_BASE}/all-rooms`)
      .then((res) => setRooms(res.data))
      .catch((err) => console.error("Error fetching rooms:", err));
  };

  const getUsers = () => {
    axios
      .get(`${API_BASE}/all-customers`)
      .then((res) => setCustomers(res.data))
      .catch((err) => console.log(err));
  };

  return (
    <div className="bg-white p-6 rounded-lg max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-4">New Room Booking</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <select
          name="customer_id"
          value={formData.customer_id}
          onChange={handleChange}
          className="border p-2 rounded w-full"
          required
        >
          <option value="" hidden>Select Customer</option>
          {customers.map((customer) => (
            <option key={customer.CustomerID} value={customer.CustomerID}>
              {customer.CustomerID}
            </option>
          ))}
        </select>

        <select
          name="room_id"
          value={formData.room_id}
          onChange={handleChange}
          className="border p-2 rounded w-full"
          required
        >
          <option value="" hidden>Select Room</option>
          {rooms.map((room) => (
            <option key={room.RoomID} value={room.RoomID}>
              {room.RoomID}
            </option>
          ))}
        </select>

        <label className="block">
          Arrival Date
          <input
            type="date"
            name="arrival_date"
            value={formData.arrival_date}
            onChange={handleChange}
            className="border p-2 rounded w-full mt-1"
            required
          />
        </label>

        <label className="block">
          Departure Date
          <input
            type="date"
            name="departure_day"
            value={formData.departure_day}
            onChange={handleChange}
            className="border p-2 rounded w-full mt-1"
            required
          />
        </label>

        <input
          name="payment_id"
          value={formData.payment_id}
          onChange={handleChange}
          placeholder="Payment ID"
          type="number"
          className="border p-2 rounded w-full"
          required
        />

        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full"
        >
          Book Room
        </button>
      </form>
    </div>
  );
};

export default NewBookingForm;
