import React from 'react';
import { BedDouble, CheckSquare, Filter, Plus } from 'lucide-react';

const roomStatus = [
  { id: 101, type: 'Standard', status: 'Occupied', guest: 'John Doe', checkOut: 'Jan 15, 2025' },
  { id: 102, type: 'Standard', status: 'Vacant', guest: null, checkOut: null },
  { id: 103, type: 'Standard', status: 'Maintenance', guest: null, checkOut: null },
  { id: 201, type: 'Deluxe', status: 'Occupied', guest: 'Jane Smith', checkOut: 'Jan 14, 2025' },
  { id: 202, type: 'Deluxe', status: 'Reserved', guest: 'Emily Davis', checkOut: null },
  { id: 203, type: 'Deluxe', status: 'Vacant', guest: null, checkOut: null },
  { id: 301, type: 'Suite', status: 'Occupied', guest: 'Sarah Brown', checkOut: 'Jan 18, 2025' },
  { id: 302, type: 'Suite', status: 'Vacant', guest: null, checkOut: null },
];

const Rooms = () => {
  return (
    <div>
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Rooms</h1>
        <div className="flex space-x-3 mt-4 md:mt-0">
          <button className="flex items-center px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
            <Filter className="h-4 w-4 mr-2" />
            <span>Filter</span>
          </button>
          <button className="flex items-center px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
            <CheckSquare className="h-4 w-4 mr-2" />
            <span>Room Status</span>
          </button>
          <button className="flex items-center px-4 py-2 bg-blue-700 text-white rounded-lg hover:bg-blue-800 transition-colors">
            <Plus className="h-4 w-4 mr-2" />
            <span>Add Room</span>
          </button>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-sm p-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {roomStatus.map((room) => (
            <div 
              key={room.id}
              className="border rounded-lg overflow-hidden hover:shadow-md transition-shadow"
            >
              <div className={`p-3 ${
                room.status === 'Occupied' ? 'bg-blue-100' :
                room.status === 'Vacant' ? 'bg-green-100' :
                room.status === 'Reserved' ? 'bg-yellow-100' :
                'bg-red-100'
              }`}>
                <div className="flex justify-between items-center">
                  <span className="font-medium">Room {room.id}</span>
                  <span 
                    className={`text-xs font-medium px-2 py-1 rounded-full ${
                      room.status === 'Occupied' ? 'bg-blue-200 text-blue-800' :
                      room.status === 'Vacant' ? 'bg-green-200 text-green-800' :
                      room.status === 'Reserved' ? 'bg-yellow-200 text-yellow-800' :
                      'bg-red-200 text-red-800'
                    }`}
                  >
                    {room.status}
                  </span>
                </div>
              </div>
              <div className="p-4">
                <div className="flex items-center text-gray-600 mb-2">
                  <BedDouble className="h-4 w-4 mr-2" />
                  <span className="text-sm">{room.type}</span>
                </div>
                {room.guest ? (
                  <div className="mt-3">
                    <p className="text-sm font-medium">{room.guest}</p>
                    <p className="text-xs text-gray-500 mt-1">Checkout: {room.checkOut}</p>
                  </div>
                ) : (
                  <p className="text-sm text-gray-500 mt-3">
                    {room.status === 'Reserved' ? 'Reserved for future guest' : 
                     room.status === 'Maintenance' ? 'Under maintenance' : 
                     'Available for booking'}
                  </p>
                )}
                <div className="mt-4 text-right">
                  <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                    View Details
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Rooms;