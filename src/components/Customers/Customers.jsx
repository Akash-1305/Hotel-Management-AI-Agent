import { Button, Card, Col, Row, Form } from "react-bootstrap";
import { useState, useEffect } from "react";
import { API_BASE } from "../../App";
import axios from "axios";
import { Plus } from "lucide-react";
import { useNavigate } from "react-router-dom";
import AddCustomer from "./AddCustomer";

export default function Customers() {
  const [customers, setCustomers] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [showForm, setShowForm] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    getUsers();
  }, []);

  function getUsers() {
    axios
      .get(`${API_BASE}/all-customers`)
      .then((res) => {
        setCustomers(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }

  const filteredCustomers = customers.filter((customer) => {
    const fullName = (
      customer.FirstName +
      " " +
      customer.LastName
    ).toLowerCase();
    return fullName.includes(searchTerm.toLowerCase());
  });

  return (
    <div className="p-3 relative">
      {/* Overlay Form */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
          <div className="bg-white p-4 rounded shadow-lg relative w-full max-w-lg">
            <button
              onClick={() => setShowForm(false)}
              className="absolute top-2 right-2 text-gray-600 hover:text-red-600 text-xl font-bold"
            >
              &times;
            </button>
            <AddCustomer
              onSuccess={() => {
                setShowForm(false);
                getUsers();
              }}
            />
          </div>
        </div>
      )}

      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Manage Customers</h1>
        <div className="flex space-x-3 mt-4 md:mt-0">
          <button
            className="flex items-center px-4 py-2 bg-blue-700 text-white rounded-lg hover:bg-blue-800 transition-colors"
            onClick={() => setShowForm(true)}
          >
            <Plus className="h-4 w-4 mr-2" />
            <span>Add Customer</span>
          </button>
        </div>
      </div>

      <Form.Group className="mb-4" controlId="search">
        <Form.Control
          type="text"
          placeholder="Search by customer name..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </Form.Group>

      <Row md={3} className="m-0 w-100">
        {filteredCustomers.length === 0 ? (
          <p>No customers found.</p>
        ) : (
          filteredCustomers.map((customer, index) => (
            <Col className="my-2" key={index}>
              <Card className="shadow bg-light">
                <Card.Body>
                  <h5 className="text-capitalize mb-3">
                    {customer.FirstName} {customer.LastName}
                  </h5>

                  <Row className="my-2">
                    <Col xs={4} className="fw-semibold text-warning">
                      Customer ID:
                    </Col>
                    <Col xs={8}>{customer.CustomerID}</Col>
                  </Row>

                  <Row className="my-2">
                    <Col xs={4} className="fw-semibold text-warning">
                      DOB:
                    </Col>
                    <Col xs={8}>{customer.DOB}</Col>
                  </Row>

                  <Row className="my-2">
                    <Col xs={4} className="fw-semibold text-warning">
                      ID Type:
                    </Col>
                    <Col xs={8}>{customer.IdentityType}</Col>
                  </Row>

                  <Row className="my-2">
                    <Col xs={4} className="fw-semibold text-warning">
                      ID Number:
                    </Col>
                    <Col xs={8}>{customer.IdentityString}</Col>
                  </Row>
                </Card.Body>
              </Card>
            </Col>
          ))
        )}
      </Row>
    </div>
  );
}
