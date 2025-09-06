import React, { useState, useEffect } from "react";
import axios from "axios";
import { BedDouble, CheckSquare, Filter, Plus } from "lucide-react";
import { API_BASE } from "../../App";
import AddRoom from "./AddRoom";

const Rooms = () => {
  const [rooms, setRooms] = useState([]);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    getAllRooms();
  }, []);

  function getAllRooms() {
    axios
      .get(API_BASE + `/all-rooms`)
      .then((res) => {
        setRooms(res.data);
      })
      .catch((err) => {
        console.error("Error fetching rooms:", err);
      });
  }

  useEffect(() => {
    getAllRooms();
  }, []);

  return (
    <div>
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Rooms</h1>
        <div className="flex space-x-3 mt-4 md:mt-0">
          <button
            className="flex items-center px-4 py-2 bg-blue-700 text-white rounded-lg hover:bg-blue-800 transition-colors"
            onClick={() => setShowModal(true)}
          >
            <Plus className="h-4 w-4 mr-2" />
            <span>Add Room</span>
          </button>
          {showModal && <AddRoom onClose={() => setShowModal(false)} />}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm p-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {rooms.map((room) => (
            <div
              key={room.RoomID}
              className="border rounded-lg overflow-hidden hover:shadow-md transition-shadow"
            >
              <div
                className={`p-3 ${
                  room.isVacant === 1 ? "bg-green-100" : "bg-red-100"
                }`}
              >
                <div className="flex justify-between items-center">
                  <span className="font-medium">Room {room.RoomID}</span>
                  <span
                    className={`text-xs font-medium px-2 py-1 rounded-full ${
                      room.isVacant === 1
                        ? "bg-green-200 text-green-800"
                        : "bg-red-200 text-red-800"
                    }`}
                  >
                    {room.isVacant === 1 ? "Vacant" : "Occupied"}
                  </span>
                </div>
              </div>
              <div className="p-4">
                <div className="flex items-center text-gray-600 mb-2">
                  <BedDouble className="h-4 w-4 mr-2" />
                  <span className="text-sm">{room.type}</span>
                </div>
                <p className="text-sm text-gray-500 mt-3">
                  {room.currentStay > 0
                    ? `Currently occupied by stay ID: ${room.currentStay}`
                    : room.isVacant === 0
                    ? "Reserved for future guest"
                    : "Available for booking"}
                </p>
                <div className="flex items-center text-gray-600 mb-2">
                  <span className="text-sm">Price: {room.price}</span>
                </div>
              </div>
            </div>
          ))}
          {rooms.length === 0 && (
            <p className="col-span-full text-gray-500 text-sm text-center">
              No rooms available.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Rooms;
