import React, { useState } from "react";
import { Search } from "lucide-react";

const ArrivalTable = ({ arrivals = [] }) => {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredArrivals = arrivals.filter(
    (arrival) =>
      arrival?.FirstName?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      arrival?.LastName?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="bg-white rounded-lg shadow-sm mt-5">
      <div className="flex justify-between items-center p-4 border-b">
        <h2 className="text-lg font-semibold">Arrivals</h2>
        <div className="flex items-center space-x-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="Search Arrivals..."
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
              <th className="px-6 py-3">Booking ID</th>
              <th className="px-6 py-3">First Name</th>
              <th className="px-6 py-3">Last Name</th>
              <th className="px-6 py-3">Arrival Date</th>
              <th className="px-6 py-3">Room Type</th>
            </tr>
          </thead>
          <tbody>
            {filteredArrivals.map((arrival) => (
              <tr
                key={arrival.BookingsID}
              >
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  {arrival.RoomID}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  {arrival.BookingsID}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  {arrival.FirstName}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  {arrival.LastName}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  {arrival.arrivalDate}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  {arrival.type}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filteredArrivals.length === 0 && (
          <div className="text-center py-4 text-gray-500 text-sm">
            No Arrivals found.
          </div>
        )}
      </div>
    </div>
  );
};

export default ArrivalTable;
