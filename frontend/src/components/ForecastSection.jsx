import { useEffect, useState } from "react";
import api from "../api/api";

export default function ForecastSection() {
  const [forecast, setForecast] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadForecast();
  }, []);

  async function loadForecast() {
    try {
      const res = await api.get("/forecast");
      setForecast(res.data.forecast);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">

      <h2 className="text-2xl font-bold mb-6">
        Sales Forecast
      </h2>

      {loading ? (
        <p>Loading forecast...</p>
      ) : (
        <table className="w-full border-collapse">

          <thead>
            <tr className="border-b">
              <th className="text-left py-2">Date</th>
              <th className="text-right py-2">Predicted Sales</th>
            </tr>
          </thead>

          <tbody>

            {forecast.slice(0, 10).map((item, index) => (
              <tr key={index} className="border-b">

                <td className="py-2">
                  {item.date}
                </td>

                <td className="text-right py-2">
                  ₹{item.predicted_sales.toLocaleString()}
                </td>

              </tr>
            ))}

          </tbody>

        </table>
      )}

    </div>
  );
}