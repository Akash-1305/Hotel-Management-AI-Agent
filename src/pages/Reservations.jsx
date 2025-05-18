import React, { useState, useEffect } from "react";
import axios from "axios";
import { Calendar, Filter, Plus } from "lucide-react";
import { API_BASE } from "../App";
import { useNavigate } from "react-router-dom";

const Reservations = () => {
  const [bookingList, setBookingList] = useState([]);
  const navigate = useNavigate();

  function getBookedRooms() {
    axios
      .get(API_BASE + `/current-stays`)
      .then((res) => {
        const transformed = res.data.map((booking) => ({
          id: booking.RoomID,
          FirstName: booking.FirstName,
          LastName: booking.LastName,
          status: booking.payment_completed === 1 ? "Arrived" : "Pending",
          room: `${booking.RoomID} (${booking.type})`,
          checkIn: booking.arrivalDate,
          checkOut: booking.departureDay,
        }));
        setBookingList(transformed);
      })
      .catch((err) => {
        console.error("Error fetching bookings:", err);
      });
  }

  useEffect(() => {
    getBookedRooms();
  }, []);

  return (
    <div>
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Reservations</h1>
        <div className="flex space-x-3 mt-4 md:mt-0">
          <button
            className="flex items-center px-4 py-2 bg-blue-700 text-white rounded-lg hover:bg-blue-800 transition-colors"
            onClick={() => navigate("/NewBooking")}
          >
            <Plus className="h-4 w-4 mr-2" />
            <span>New Reservation</span>
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm">
        <div className="p-4 border-b">
          <h2 className="text-lg font-semibold">All Reservations</h2>
        </div>
        <div className="p-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {bookingList.map((booking) => (
              <div
                key={booking.id}
                className="border rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start">
                  <h3 className="font-medium">
                    {booking.FirstName} {booking.LastName}
                  </h3>
                  <span
                    className={`text-xs font-medium px-2 py-1 rounded-full ${
                      booking.status === "Arrived"
                        ? "bg-green-100 text-green-800"
                        : "bg-blue-100 text-blue-800"
                    }`}
                  >
                    {booking.status}
                  </span>
                </div>
                <div className="mt-2 text-sm text-gray-600">
                  <p>Room: {booking.room}</p>
                  <p className="mt-1">Check In: {booking.checkIn}</p>
                  <p className="mt-1">Check Out: {booking.checkOut}</p>
                </div>
                <div className="mt-4 text-right">
                  <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                    View Details
                  </button>
                </div>
              </div>
            ))}
            {bookingList.length === 0 && (
              <p className="text-gray-500 text-sm col-span-full">
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
