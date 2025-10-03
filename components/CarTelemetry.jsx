import React, { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import "../Telemetry.css";

// --- UI Components ---
function UserCard() {
  return (
    <div className="rounded-2xl bg-white p-4 shadow-sm border border-slate-200 mb-2 flex items-center gap-3">
      <div className="h-12 w-12 rounded-full bg-gradient-to-tr from-blue-500 to-sky-500 text-white flex items-center justify-center font-semibold">
        C
      </div>
      <div>
        <div className="font-medium">Car Telemetry</div>
        <div className="text-xs text-slate-500">Live Data</div>
      </div>
    </div>
  );
}

function SideLink({ label, active = false }) {
  return (
    <button
      className={
        "w-full text-left px-4 py-2 rounded-xl text-sm border " +
        (active
          ? "bg-blue-50 border-blue-200 text-blue-700"
          : "bg-white border-slate-200 text-slate-700 hover:bg-slate-50")
      }
    >
      {label}
    </button>
  );
}

function LegendDot({ className = "", label }) {
  return (
    <div className="flex items-center gap-2">
      <span className={`inline-block h-3 w-3 rounded-full ${className}`}></span>
      <span className="text-slate-500">{label}</span>
    </div>
  );
}

function BarChart({ data }) {
  const max = Math.max(
    ...data.series.Temp,
    ...data.series.Precip,
    ...data.series.Sunlight
  );
  return (
    <div>
      <div className="grid grid-cols-4 gap-4 h-56 items-end">
        {data.labels.map((label, idx) => (
          <div key={label} className="flex flex-col items-center gap-2">
            <div className="flex items-end gap-1 h-full w-full">
              <div
                className="flex-1 rounded-sm bg-yellow-500/80"
                style={{
                  height: `${(data.series.Temp[idx] / max) * 100}%`,
                }}
              />
              <div
                className="flex-1 rounded-sm bg-sky-500/80"
                style={{
                  height: `${(data.series.Precip[idx] / max) * 100}%`,
                }}
              />
              <div
                className="flex-1 rounded-sm bg-emerald-500/80"
                style={{
                  height: `${(data.series.Sunlight[idx] / max) * 100}%`,
                }}
              />
            </div>
            <div className="text-[10px] text-slate-500">{label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function DonutChart({ data }) {
  const total = data.reduce((sum, d) => sum + d.value, 0);
  const angles = data.map((d) => (d.value / total) * 360);
  const gradient = `conic-gradient(
    #facc15 0 ${angles[0]}deg,
    #60a5fa ${angles[0]}deg ${angles[0] + angles[1]}deg,
    #34d399 ${angles[0] + angles[1]}deg ${
    angles[0] + angles[1] + angles[2]
  }deg,
    #f87171 ${angles[0] + angles[1] + angles[2]}deg 360deg
  )`;
  return (
    <div className="flex items-center justify-center">
      <div
        className="h-48 w-48 rounded-full"
        style={{ background: gradient, position: "relative" }}
      >
        <div className="absolute inset-6 bg-white rounded-full grid place-items-center text-slate-600 text-sm">
          Weather
        </div>
      </div>
    </div>
  );
}

function donutColor(i) {
  return (
    ["bg-yellow-500", "bg-sky-500", "bg-emerald-500", "bg-red-400"][i] ||
    "bg-slate-400"
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
        { time: new Date().toLocaleTimeString(), speed: newData.speed },
      ]);
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="telemetry-container">
      <UserCard />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Telemetry Info */}
        <div>
          <h2 className="telemetry-title">🚘 Car Telemetry</h2>
          <div className="telemetry-grid">
            <div className="telemetry-card">
              <p className="label">Speed</p>
              <p className="value">{data.speed} km/h</p>
            </div>
            <div className="telemetry-card">
              <p className="label">Engine Temp</p>
              <p className="value">{data.engineTemp} °C</p>
            </div>
            <div className="telemetry-card">
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
                  stroke="#2563eb"
                  strokeWidth={2}
                  dot={true}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Weather Visuals */}
        <div>
          <h2 className="telemetry-title">🌦 Weather Overview</h2>
          <DonutChart
            data={[
              { label: "Temp", value: 30 },
              { label: "Precip", value: 20 },
              { label: "Sunlight", value: 40 },
              { label: "Wind", value: 10 },
            ]}
          />

          <div className="mt-4">
            <LegendDot className="bg-yellow-500" label="Temp" />
            <LegendDot className="bg-sky-500" label="Precip" />
            <LegendDot className="bg-emerald-500" label="Sunlight" />
            <LegendDot className="bg-red-400" label="Wind" />
          </div>
        </div>
      </div>
    </div>
  );
}