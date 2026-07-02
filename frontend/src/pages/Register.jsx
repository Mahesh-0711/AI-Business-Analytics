import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import api from "../api/api";

export default function Register() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  async function handleRegister(e) {
    e.preventDefault();

    setLoading(true);

    try {
      await api.post("/register", formData);

      alert("Registration successful!");

      navigate("/login");
    } catch (err) {
      alert(err.response?.data?.detail || "Registration failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center">

      <form
        onSubmit={handleRegister}
        className="bg-white shadow-xl rounded-xl p-8 w-96"
      >

        <h1 className="text-3xl font-bold text-center mb-6">
          Create Account
        </h1>

        <input
          type="text"
          name="name"
          placeholder="Full Name"
          value={formData.name}
          onChange={handleChange}
          className="w-full border rounded-lg p-3 mb-4"
          required
        />

        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          className="w-full border rounded-lg p-3 mb-4"
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          className="w-full border rounded-lg p-3 mb-6"
          required
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700"
        >
          {loading ? "Creating Account..." : "Register"}
        </button>

        <div className="text-center mt-5">
          <Link
            to="/login"
            className="text-blue-600"
          >
            Already have an account?
          </Link>
        </div>

      </form>

    </div>
  );
}