import { useEffect, useState } from "react";
import api from "../api/api";

export default function AIInsightsSection() {
  const [analysis, setAnalysis] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadInsights();
  }, []);

  async function loadInsights() {
    try {
      const res = await api.get("/ai-insights");
      setAnalysis(res.data.ai_analysis);
    } catch (err) {
      console.error(err);
      setAnalysis("Unable to generate AI insights.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">

      <h2 className="text-2xl font-bold mb-6">
        AI Business Insights
      </h2>

      {loading ? (
        <p className="text-gray-500">Generating insights...</p>
      ) : (
        <div className="whitespace-pre-wrap text-gray-700 leading-7">
          {analysis}
        </div>
      )}

    </div>
  );
}