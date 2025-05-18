import React, { useState } from "react";
import { Search, SlidersHorizontal, MoreVertical } from "lucide-react";

const BookingsTable = ({ bookings = [] }) => {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredBookings = bookings.filter(
    (booking) =>
      booking?.FirstName?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      booking?.LastName?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="bg-white rounded-lg shadow-sm">
      <div className="flex justify-between items-center p-4 border-b">
        <h2 className="text-lg font-semibold">Occupied Rooms</h2>
        <div className="flex items-center space-x-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="Search Occupied Rooms..."
              className="pl-10 pr-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              <th className="px-6 py-3">Room ID</th>
              <th className="px-6 py-3">First Name</th>
              <th className="px-6 py-3">Last Name</th>
              <th className="px-6 py-3">Check In</th>
              <th className="px-6 py-3">Check Out</th>
              <th className="px-6 py-3">Price</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filteredBookings.map((booking) => {
              const status = booking.payment_completed
                ? "Completed"
                : "Reserved";
              return (
                <tr
                  key={booking.RoomID}
                  className="hover:bg-gray-50 transition-colors"
                >
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    {booking.RoomID}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    {booking.FirstName}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    {booking.LastName}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    {booking.arrivalDate}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    {booking.departureDay}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-800">
                    ${booking.price}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {filteredBookings.length === 0 && (
          <div className="text-center py-4 text-gray-500 text-sm">
            No occupied rooms found.
          </div>
        )}
      </div>
    </div>
  );
};

export default BookingsTable;
