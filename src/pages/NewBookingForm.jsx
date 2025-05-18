import React, { useState } from "react";
import axios from "axios";
import { API_BASE } from "../App";

const NewBookingForm = () => {
  const [formData, setFormData] = useState({
    RoomID: "",
    type: "",
    price: "",
    FirstName: "",
    LastName: "",
    arrivalDate: "",
    departureDay: "",
    booking_price: "",
    discount: "",
    PaymentType: "",
    payment_completed: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Sending all data in a single POST to /book-room
      const payload = {
        RoomID: parseInt(formData.RoomID),
        type: formData.type,
        price: parseFloat(formData.price),
        FirstName: formData.FirstName,
        LastName: formData.LastName,
        arrivalDate: formData.arrivalDate,
        departureDay: formData.departureDay,
        booking_price: parseFloat(formData.booking_price),
        discount: parseFloat(formData.discount) || 0,
        PaymentType: formData.PaymentType,
        payment_completed: formData.payment_completed ? 1 : 0,
      };

      await axios.post(`${API_BASE}/book-room`, payload);

      alert("Room booked successfully!");
      setFormData({
        RoomID: "",
        type: "",
        price: "",
        FirstName: "",
        LastName: "",
        arrivalDate: "",
        departureDay: "",
        booking_price: "",
        discount: "",
        PaymentType: "",
        payment_completed: false,
      });
    } catch (err) {
      console.error("Booking error:", err);
      alert("Error during booking. Check console.");
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md max-w-2xl mx-auto">
      <h2 className="text-xl font-bold mb-4">New Room Booking</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input
            name="FirstName"
            value={formData.FirstName}
            onChange={handleChange}
            placeholder="First Name"
            className="border p-2 rounded"
            required
          />
          <input
            name="LastName"
            value={formData.LastName}
            onChange={handleChange}
            placeholder="Last Name"
            className="border p-2 rounded"
            required
          />
          <input
            name="RoomID"
            value={formData.RoomID}
            onChange={handleChange}
            placeholder="Room ID"
            type="number"
            className="border p-2 rounded"
            required
          />
          <input
            name="type"
            value={formData.type}
            onChange={handleChange}
            placeholder="Room Type (e.g., 2BHK)"
            className="border p-2 rounded"
            required
          />
          <input
            name="price"
            value={formData.price}
            onChange={handleChange}
            placeholder="Room Price"
            type="number"
            className="border p-2 rounded"
            required
          />
          <input
            name="booking_price"
            value={formData.booking_price}
            onChange={handleChange}
            placeholder="Booking Price"
            type="number"
            className="border p-2 rounded"
            required
          />
          <input
            name="discount"
            value={formData.discount}
            onChange={handleChange}
            placeholder="Discount (%)"
            type="number"
            className="border p-2 rounded"
          />
          <select
            name="PaymentType"
            value={formData.PaymentType}
            onChange={handleChange}
            className="border p-2 rounded"
            required
          >
            <option value="">Select Payment Type</option>
            <option value="Credit Card">Credit Card</option>
            <option value="Cash">Cash</option>
            <option value="UPI">UPI</option>
            <option value="Bank Transfer">Bank Transfer</option>
          </select>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <label className="text-sm font-medium">
            Arrival Date
            <input
              type="date"
              name="arrivalDate"
              value={formData.arrivalDate}
              onChange={handleChange}
              className="border p-2 w-full rounded mt-1"
              required
            />
          </label>
          <label className="text-sm font-medium">
            Departure Date
            <input
              type="date"
              name="departureDay"
              value={formData.departureDay}
              onChange={handleChange}
              className="border p-2 w-full rounded mt-1"
              required
            />
          </label>
        </div>

        <label className="flex items-center space-x-2">
          <input
            type="checkbox"
            name="payment_completed"
            checked={formData.payment_completed}
            onChange={handleChange}
          />
          <span>Payment Completed</span>
        </label>

        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Book Room
        </button>
      </form>
    </div>
  );
};

export default NewBookingForm;
