import React, { use } from "react";
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
} from "recharts";
import "../index.css";

// --- UI Components ---
function UserCard() {
    return (
        <div className="rounded-2x1 bg-white p-4 shadow-sm border border-slate-200 mb-2 flex items-center gap-3">
            <div className="h-12 w-12 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500 text-white flex items-center justify-center font-semibold">
                C
            </div>
            <div>
                <div className="font-semibold text-slate-800">Car Telemetry</div>
                <div className="text-sm text-slate-500">Real-time Data</div>
            </div>
        </div>
    );
}

// --- Main Car Telemetry Component ---
export default function Dashboard() {
  const [data, setData] = useState({
    speed: 0,
    engineTemp: 0,
    batteryLevel: 0,
  });
  const [history, setHistory] = useState([]);

  const generateTelemetry = () => ({
    speed: parseFloat((Math.random() * 120).toFixed(1)),
    engineTemp: parseFloat((70 + Math.random() * 30).toFixed(1)),
    batteryLevel: parseInt(Math.random() * 100),
  });

  useEffect(() => {
    const interval = setInterval(() => {
      const newData = generateTelemetry();
      setData(newData);
      setHistory((prev) => [
        ...prev.slice(-9),
        { time: new Date().toLocaleTimeString(), speed: newData.speed, engineTemp: newData.engineTemp, batteryLevel: newData.batteryLevel },
      ]);
    }, 3000);

    return () => clearInterval(interval);
  }, []);
  return (
    <div className="telemetry-container">
      <UserCard />

      <div className="grid grid-cols-1 md:grid-cols-1 gap-6">
        {/* Telemetry Info */}
        <div>
          <div className="telemetry-grid">
            <div className="rounded-xl bg-white p-4 shadow-sm border border-slate-200 p-4 text center inline-block">
              <p className="label">Speed</p>
              <p className="value">{data.speed} km/h</p>
            </div>
            <div className="rounded-xl bg-white p-4 shadow-sm border border-slate-200 p-4 text center inline-block">
              <p className="label">Engine Temp</p>
              <p className="value">{data.engineTemp} °C</p>
            </div>
            <div className="rounded-xl bg-white p-4 shadow-sm border border-slate-200 p-4 text center inline-block">
              <p className="label">Battery</p>
              <p className="value">{data.batteryLevel}%</p>
            </div>
          </div>

          <div className="telemetry-chart">
            <p className="chart-title">Speed History</p>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis domain={[0, 120]} />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="speed"
                  stroke="#8e25f0ff"
                  strokeWidth={2}
                  dot={true}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="telemetry-chart">
            <p className="chart-title">Engine Temp History</p>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis domain={[0, 200]} />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="engineTemp"
                  stroke="#8e25f0ff"
                  strokeWidth={2}
                  dot={true}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="telemetry-chart">
            <p className="chart-title">Battery History</p>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="batteryLevel"
                  stroke="#8e25f0ff"
                  strokeWidth={2}
                  dot={true}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}