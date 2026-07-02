import { NavLink } from "react-router-dom";

const menu = [
  { name: "Dashboard", path: "/dashboard" },
  { name: "Upload", path: "/upload" },
  { name: "Profile", path: "/profile" },
  { name: "KPIs", path: "/kpis" },
  { name: "Charts", path: "/charts" },
  { name: "AI Insights", path: "/ai-insights" },
  { name: "Chat", path: "/chat" },
  { name: "Forecast", path: "/forecast" },
  { name: "My Datasets", path: "/my-datasets" },
];

export default function Sidebar() {

  return (

    <aside className="w-64 bg-white shadow min-h-screen">

      <div className="p-5">

        {menu.map((item) => (

          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `block p-3 rounded-lg mb-2 ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "hover:bg-gray-100"
              }`
            }
          >
            {item.name}
          </NavLink>

        ))}

      </div>

    </aside>

  );

}