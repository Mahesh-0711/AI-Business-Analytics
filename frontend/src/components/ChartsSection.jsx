import Plot from "react-plotly.js";
import ChartCard from "./ChartCard";

export default function ChartsSection({ charts }) {

  if (!charts) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8">
        Loading Charts...
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">

      <h2 className="text-2xl font-bold mb-6">
        Interactive Charts
      </h2>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">

        {/* Sales by Region */}

        <ChartCard title="Sales by Region">

          <Plot
            data={[
              {
                x: charts.sales_by_region?.labels,
                y: charts.sales_by_region?.values,
                type: "bar",
                marker: {
                  color: "#3b82f6"
                }
              }
            ]}
            layout={{
              autosize: true,
              margin: {
                t: 30,
                l: 40,
                r: 20,
                b: 40
              }
            }}
            style={{
              width: "100%",
              height: "350px"
            }}
          />

        </ChartCard>

        {/* Sales by Category */}

        <ChartCard title="Sales by Category">

          <Plot
            data={[
              {
                labels: charts.sales_by_category?.labels,
                values: charts.sales_by_category?.values,
                type: "pie"
              }
            ]}
            layout={{
              autosize: true
            }}
            style={{
              width: "100%",
              height: "350px"
            }}
          />

        </ChartCard>

        {/* Profit */}

        <ChartCard title="Profit by Category">

          <Plot
            data={[
              {
                x: charts.profit_by_category?.labels,
                y: charts.profit_by_category?.values,
                type: "bar",
                marker: {
                  color: "#16a34a"
                }
              }
            ]}
            layout={{
              autosize: true,
              margin: {
                t: 30
              }
            }}
            style={{
              width: "100%",
              height: "350px"
            }}
          />

        </ChartCard>

        {/* Monthly Sales */}

        <ChartCard title="Monthly Sales">

          <Plot
            data={[
              {
                x: charts.monthly_sales?.labels,
                y: charts.monthly_sales?.values,
                type: "scatter",
                mode: "lines+markers"
              }
            ]}
            layout={{
              autosize: true,
              margin: {
                t: 30
              }
            }}
            style={{
              width: "100%",
              height: "350px"
            }}
          />

        </ChartCard>

      </div>

    </div>
  );
}