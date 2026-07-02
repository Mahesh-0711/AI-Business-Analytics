import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

import api from "../api/api";
import { useAuth } from "../context/AuthContext";

export default function Login() {

  const navigate = useNavigate();

  const { login } = useAuth();

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  async function handleLogin(e) {

    e.preventDefault();

    setLoading(true);

    try {

      const res = await api.post("/login", {
        email,
        password
      });

      login(
        res.data.user,
        res.data.access_token
      );

      navigate("/dashboard");

    } catch (err) {

      alert(
        err.response?.data?.detail ||
        "Login failed."
      );

    } finally {

      setLoading(false);

    }

  }

  return (

    <div className="min-h-screen bg-slate-100 flex items-center justify-center">

      <form
        onSubmit={handleLogin}
        className="bg-white shadow-xl rounded-xl p-8 w-96"
      >

        <h1 className="text-3xl font-bold text-center mb-6">
          Login
        </h1>

        <input
          type="email"
          placeholder="Email"
          className="w-full border rounded-lg p-3 mb-4"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full border rounded-lg p-3 mb-6"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
        />

        <button
          className="bg-blue-600 text-white w-full py-3 rounded-lg"
          disabled={loading}
        >
          {loading ? "Logging in..." : "Login"}
        </button>

        <div className="text-center mt-5">

          <Link
            to="/register"
            className="text-blue-600"
          >
            Create Account
          </Link>

        </div>

      </form>

    </div>

  );

}