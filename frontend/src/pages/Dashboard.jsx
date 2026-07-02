import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

import KPICard from "../components/KPICard";
import InfoCard from "../components/InfoCard";
import ChartsSection from "../components/ChartsSection";
import AIInsightsSection from "../components/AIInsightsSection";
import ForecastSection from "../components/ForecastSection";
import ChatSection from "../components/ChatSection";

export default function Dashboard() {
  const navigate = useNavigate();

  const [kpis, setKpis] = useState(null);
  const [profile, setProfile] = useState(null);
  const [charts, setCharts] = useState(null);

  const [loading, setLoading] = useState(true);
  const [noDataset, setNoDataset] = useState(false);

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    try {
      const [kpiRes, profileRes, chartRes] = await Promise.all([
        api.get("/kpis"),
        api.get("/profile"),
        api.get("/charts"),
      ]);

      setKpis(kpiRes.data);
      setProfile(profileRes.data);
      setCharts(chartRes.data);

      setNoDataset(false);
    } catch (err) {
      if (err.response?.status === 400) {
        setNoDataset(true);
      } else {
        console.error(err);
      }
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-[70vh]">
        <h2 className="text-2xl font-semibold text-gray-600">
          Loading Dashboard...
        </h2>
      </div>
    );
  }

  if (noDataset) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-10 text-center">

        <h1 className="text-3xl font-bold mb-4">
          Welcome to AI Business Analytics
        </h1>

        <p className="text-lg text-gray-600">
          No dataset uploaded.
        </p>

        <p className="mt-4 text-gray-500 mb-8">
          Upload a CSV dataset to begin analysis.
        </p>

        <button
          onClick={() => navigate("/upload")}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg"
        >
          Upload Dataset
        </button>

      </div>
    );
  }

  return (
    <div className="space-y-8">

      {/* Header */}

      <div>
        <h1 className="text-3xl font-bold text-gray-800">
          Business Dashboard
        </h1>

        <p className="text-gray-500 mt-2">
          AI-powered analytics dashboard
        </p>
      </div>

      {/* KPI Cards */}

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

        <KPICard
          title="Total Sales"
          value={`₹${Number(kpis["Total Sales"]).toLocaleString()}`}
          color="text-blue-600"
        />

        <KPICard
          title="Total Profit"
          value={`₹${Number(kpis["Total Profit"]).toLocaleString()}`}
          color="text-green-600"
        />

        <KPICard
          title="Total Orders"
          value={kpis["Total Orders"]}
          color="text-purple-600"
        />

        <KPICard
          title="Average Sale"
          value={`₹${Math.round(
            Number(kpis["Average Sale"])
          ).toLocaleString()}`}
          color="text-orange-600"
        />

      </div>

      {/* Dataset Summary */}

      <div className="bg-white rounded-xl shadow-lg p-6">

        <h2 className="text-2xl font-semibold mb-6">
          Dataset Summary
        </h2>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-5">

          <InfoCard
            title="Rows"
            value={profile.rows}
          />

          <InfoCard
            title="Columns"
            value={profile.columns}
          />

          <InfoCard
            title="Missing Values"
            value={profile.missing_values}
          />

          <InfoCard
            title="Duplicate Rows"
            value={profile.duplicate_rows}
          />

        </div>

      </div>

      {/* Charts */}

      <ChartsSection charts={charts} />

      {/* AI Insights */}

      <AIInsightsSection />

      {/* Forecast */}

      <ForecastSection />

      {/* Chat */}

      <ChatSection />

    </div>
  );
}