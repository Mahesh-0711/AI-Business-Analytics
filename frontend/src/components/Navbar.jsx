import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {

  const navigate = useNavigate();

  const { user, logout } = useAuth();

  function handleLogout() {

    logout();

    navigate("/login");

  }

  return (

    <nav className="bg-blue-700 text-white px-8 py-4 flex justify-between items-center shadow">

      <h1 className="text-2xl font-bold">
        AI Business Analytics
      </h1>

      <div className="flex items-center gap-6">

        <span>
          Welcome, <strong>{user?.name}</strong>
        </span>

        <button
          onClick={handleLogout}
          className="bg-red-500 px-4 py-2 rounded-lg hover:bg-red-600"
        >
          Logout
        </button>

      </div>

    </nav>

  );

}