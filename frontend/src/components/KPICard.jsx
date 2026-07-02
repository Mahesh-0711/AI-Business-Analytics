export default function KPICard({
    title,
    value,
    color
}) {

    return (

        <div className="bg-white rounded-xl shadow-lg p-6">

            <h3 className="text-gray-500">
                {title}
            </h3>

            <p className={`text-3xl font-bold mt-3 ${color}`}>
                {value}
            </p>

        </div>

    );

}