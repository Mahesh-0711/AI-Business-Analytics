export default function ChartCard({ title, children }) {
  return (
    <div className="bg-slate-50 rounded-xl border p-5">

      <h3 className="text-lg font-semibold mb-4">
        {title}
      </h3>

      {children}

    </div>
  );
}