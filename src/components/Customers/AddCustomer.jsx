import axios from "axios";
import { useState } from "react";

const AddCustomer = () => {
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [dob, setDob] = useState("");
  const [identity_type, setIdentityType] = useState("");
  const [identity_string, setIdentityString] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await axios.post("http://127.0.0.1:8000/add-customer", null, {
        params: {
          first_name,
          last_name,
          dob,
          identity_type,
          identity_string,
        },
      });
      alert("Customer added successfully");
      setFirstName("");
      setLastName("");
      setDob("");
      setIdentityType("");
      setIdentityString("");
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong!");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto p-4">
      <input
        type="text"
        placeholder="First Name"
        value={first_name}
        onChange={(e) => setFirstName(e.target.value)}
        className="w-full border p-2 rounded"
        required
      />
      <input
        type="text"
        placeholder="Last Name"
        value={last_name}
        onChange={(e) => setLastName(e.target.value)}
        className="w-full border p-2 rounded"
        required
      />
      <input
        type="date"
        value={dob}
        onChange={(e) => setDob(e.target.value)}
        className="w-full border p-2 rounded"
        required
      />
      <input
        type="text"
        placeholder="Identity Type"
        value={identity_type}
        onChange={(e) => setIdentityType(e.target.value)}
        className="w-full border p-2 rounded"
        required
      />
      <input
        type="text"
        placeholder="Identity Number"
        value={identity_string}
        onChange={(e) => setIdentityString(e.target.value)}
        className="w-full border p-2 rounded"
        required
      />
      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Add Customer
      </button>
    </form>
  );
};

export default AddCustomer;
