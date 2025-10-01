import React, {useEffect, useState} from "react";
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer} from "react";

export default function carTelem(){
    const [data, setData] = useState({
        speed: 0,
        engineTemp: 0,
        batteryLevel: 0,
    });

    const [history, setHistory] = useState([]);
    
    //function to simulate telemetry updates
    const generateTelemetry = () => {
        return {
            speed: parseFloat((Math.random() * 120).toFixed(1)),            // km/h
            engineTemp: parseFloat((70 + Math.random() * 30).toFixed(1)),   // °C
            batteryLevelL: parseInt(Math.random() * 100),                   // %
        };
    };

    useEffect(() => {
        // Update every 3 seconds
        const interval = setInterval(() => {
            const newData = generateTelemetry();
            setData(newData);

            // keep a rolling history of last 10 updates
            setHistory((prev) => {
                const updated = [...prev, {time: new Date().toLocaleTimeString(), speed: newData.speed}];
                return updated.slice(-10);
            });
        }, 3000);

        return () => clearInterval(interval);
    }, []);

    return (
    <div className="p-6 bg-white rounded-2xl shadow-md w-full max-w-2xl">
      <h2 className="text-xl font-bold mb-4 text-gray-800">🚘 Car Telemetry</h2>

      {/* Info Panel */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="p-3 bg-gray-100 rounded-lg">
          <p className="text-gray-600">Speed</p>
          <p className="text-lg font-semibold">{data.speed} km/h</p>
        </div>
        <div className="p-3 bg-gray-100 rounded-lg">
          <p className="text-gray-600">Engine Temp</p>
          <p className="text-lg font-semibold">{data.engineTemp} °C</p>
        </div>
        <div className="p-3 bg-gray-100 rounded-lg">
          <p className="text-gray-600">Battery</p>
          <p className="text-lg font-semibold">{data.batteryLevel}%</p>
        </div>
      </div>

      {/* chart */}
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={history}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis domain={[0, 120]} label={{ value: "km/h", angle: -90, position: "insideLeft" }} />
            <Tooltip />
            <Line type="monotone" dataKey="speed" stroke="#2563eb" strokeWidth={2} dot={true} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}