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

export default function CarTelemetry() {
  const [data, setData] = useState({
    speed: 0,
    engineTemp: 0,
    batteryLevel: 0,
  });

  const [history, setHistory] = useState([]);

  // Function to simulate telemetry updates
  const generateTelemetry = () => {
    return {
      speed: parseFloat((Math.random() * 120).toFixed(1)), // km/h
      engineTemp: parseFloat((70 + Math.random() * 30).toFixed(1)), // °C
      batteryLevel: parseInt(Math.random() * 100), // %
    };
  };

  useEffect(() => {
    // Update every 3 seconds
    const interval = setInterval(() => {
      const newData = generateTelemetry();
      setData(newData);

      // Keep a rolling history of last 10 updates
      setHistory((prev) => {
        const updated = [
          ...prev,
          { time: new Date().toLocaleTimeString(), speed: newData.speed },
        ];
        return updated.slice(-10);
      });
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="telemetry-container">
      <h2 className="telemetry-title">Car Telemetry</h2>

      {/* Info Panel */}
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

      {/* Chart */}
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
  );
}