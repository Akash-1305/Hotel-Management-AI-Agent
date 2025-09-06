import React, { useState, useEffect } from "react";
import axios from "axios";
import { Plus, X } from "lucide-react";
import { API_BASE } from "../../App";
import { useNavigate } from "react-router-dom";
import NewBookingForm from "./NewBookingForm";

const Reservations = () => {
  const [bookingList, setBookingList] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const navigate = useNavigate();

  // Get today's date in YYYY-MM-DD format
  const getTodayDate = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  };

  const today = getTodayDate();

  // Convert any date string to YYYY-MM-DD format for easy comparison
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  };

  useEffect(() => {
    getBookedRooms();
  }, []);

  function getBookedRooms() {
    axios
      .get(API_BASE + `/all-bookings`)
      .then((res) => {
        setBookingList(res.data);
      })
      .catch((err) => {
        console.error("Error fetching bookings:", err);
      });
  }

  const handleCheckIn = (booking) => {
    axios
      .post(
        `${API_BASE}/check-in?room_id=${booking.RoomID}&booking_id=${booking.BookingsID}`
      )
      .then(() => {
        alert("Checked in successfully!");
        getBookedRooms();
      })
      .catch((err) => {
        console.error("Check-in failed:", err);
        alert(err.response?.data?.message);
      });
  };

  const handleCheckOut = (roomId) => {
    axios
      .post(`${API_BASE}/check-out?room_id=${roomId}`)
      .then(() => {
        alert("Checked out successfully!");
        getBookedRooms();
      })
      .catch((err) => {
        console.error("Check-out failed:", err);
        alert(err.response?.data?.message);
      });
  };

  const handleCancel = (bookingId) => {
    if (!window.confirm("Are you sure you want to cancel this booking?"))
      return;

    axios
      .delete(`${API_BASE}/cancel-booking?booking_id=${bookingId}`)
      .then(() => {
        alert("Booking cancelled.");
        getBookedRooms();
      })
      .catch((err) => {
        console.error("Cancellation failed:", err);
        alert("Cancellation failed.");
      });
  };

  return (
    <div>
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Reservations</h1>
        <button
          className="flex items-center px-4 py-2 bg-blue-700 text-white rounded-lg hover:bg-blue-800 transition-colors mb-4"
          onClick={() => setShowForm(true)}
        >
          <Plus className="h-4 w-4 mr-2" />
          <span>New Reservation</span>
        </button>
      </div>

      {showForm && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
          onClick={() => setShowForm(false)}
        >
          <div
            className="bg-white rounded-lg shadow-lg p-6 w-full max-w-2xl relative"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              className="absolute top-3 right-3 text-gray-600 hover:text-gray-900"
              onClick={() => setShowForm(false)}
              aria-label="Close form"
            >
              <X className="h-6 w-6" />
            </button>
            <NewBookingForm onClose={() => setShowForm(false)} />
          </div>
        </div>
      )}

      <div className="bg-white rounded-lg shadow-sm">
        <div className="p-4 border-b">
          <h2 className="text-lg font-semibold">All Reservations</h2>
        </div>
        <div className="p-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {bookingList.map((booking) => (
              <div
                key={booking.BookingsID}
                className="border rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="mt-2 text-sm text-gray-600">
                  <h3 className="font-medium text-black">
                    Booking ID: {booking.BookingsID}
                  </h3>
                  <p className="mt-1">Room ID: {booking.RoomID}</p>
                  <p className="mt-1">Customer ID: {booking.customerID}</p>
                  <p className="mt-1">Room Type: {booking.room_type}</p>
                  <p className="mt-1">Booked Date: {booking.bookedDate}</p>
                  <p className="mt-1">Arrival Date: {booking.arrivalDate}</p>
                  <p className="mt-1">Departure Day: {booking.departureDay}</p>
                  <p className="mt-1">Payment ID: {booking.paymentID}</p>
                </div>

                <div className="flex gap-2 mt-4 justify-center">
                  {formatDate(booking.arrivalDate) <= today && (
                    <button
                      onClick={() => handleCheckIn(booking)}
                      className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
                    >
                      Check-In
                    </button>
                  )}
                  {formatDate(booking.arrivalDate) <= today && (
                    <button
                      onClick={() => handleCheckOut(booking.RoomID)}
                      className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
                    >
                      Check-Out
                    </button>
                  )}
                  <button
                    onClick={() => handleCancel(booking.BookingsID)}
                    className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ))}
            {bookingList.length === 0 && (
              <p className="text-blue-500 text-sm col-span-full">
                No reservations found.
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reservations;
