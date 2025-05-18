import React, { useState } from "react";
import axios from "axios";
import { X } from "lucide-react";
import { API_BASE } from "../../App";

const AddRoom = ({ onClose }) => {
  const [formData, setFormData] = useState({
    room_id: "",
    room_type: "",
    price: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);

    const params = {
      room_id: parseInt(formData.room_id),
      room_type: formData.room_type,
      price: parseFloat(formData.price),
    };

    axios
      .post(`${API_BASE}/add-room`, null, { params })
      .then((res) => {
        alert("Room added successfully!");
        setFormData({ room_id: "", room_type: "", price: "" });
        if (onClose) onClose();
      })
      .catch((err) => {
        console.error("Error booking room:", err);
        alert("Failed to add the room.");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-lg shadow-lg p-6 w-full max-w-lg relative"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          className="absolute top-3 right-3 text-gray-600 hover:text-gray-900"
          onClick={onClose}
        >
          <X className="h-6 w-6" />
        </button>

        <h2 className="text-xl font-semibold mb-4">Add New Room</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Room ID
            </label>
            <input
              type="number"
              name="room_id"
              value={formData.room_id}
              onChange={handleChange}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Room Type (2BHK or 3BHK)
            </label>
            <input
              type="text"
              name="room_type"
              value={formData.room_type}
              onChange={handleChange}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Price
            </label>
            <input
              type="number"
              name="price"
              value={formData.price}
              onChange={handleChange}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            />
          </div>

          <div className="flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              disabled={loading}
            >
              {loading ? "Submitting..." : "Submit"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddRoom;
