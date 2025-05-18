import React, { useState } from "react";
import axios from "axios";
import { API_BASE } from "../../App";

function AddCustomer({ onSuccess }) {
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    dob: "",
    identity_type: "",
    identity_string: "",
  });

  const [message, setMessage] = useState("");

  const clearFields = () => {
    setFormData({
      first_name: "",
      last_name: "",
      dob: "",
      identity_type: "",
      identity_string: "",
    });
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Sending data:", formData); // Debugging log

    try {
      // ✅ Send data as query parameters
      const response = await axios.post(`${API_BASE}/add-customer`, null, {
        params: formData,
        headers: { "Content-Type": "application/json" },
      });

      console.log(response);
      clearFields();
      setMessage("Customer added successfully!");
      if (onSuccess) onSuccess(response.data);
    } catch (err) {
      const errorMsg = err.response?.data || {
        detail: "Something went wrong!",
      };
      console.error("Server Response:", errorMsg);

      // ✅ Show error message
      setMessage(
        typeof errorMsg === "object"
          ? JSON.stringify(errorMsg)
          : errorMsg.detail || "Something went wrong!"
      );
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 rounded">
      <h2 className="text-xl font-bold mb-2">Add New Customer</h2>

      {["first_name", "last_name", "identity_type", "identity_string"].map(
        (field) => (
          <input
            key={field}
            name={field}
            placeholder={field.replace("_", " ").toUpperCase()}
            value={formData[field]}
            onChange={handleChange}
            className="w-full p-2 border rounded"
            required
          />
        )
      )}

      <input
        type="date"
        name="dob"
        value={formData.dob}
        onChange={handleChange}
        className="w-full p-2 border rounded"
        required
      />

      {/* ✅ Show success or error message */}
      {message && (
        <div className="text-sm text-red-600 font-semibold">{message}</div>
      )}

      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Add Customer
      </button>
    </form>
  );
}

export default AddCustomer;
