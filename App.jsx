import React, { useMemo, useState } from "react";

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Example "stats" for weather and routes
  const stats = [
    { title: "Temperature", value: "24°C", change: "+2°C", gradient: "from-yellow-400 to-orange-500" },
    { title: "Precipitation", value: "20%", change: "-5%", gradient: "from-sky-400 to-blue-600" },
    { title: "Air Quality", value: "Good (45 AQI)", change: "+3%", gradient: "from-emerald-400 to-teal-500" },
  ];

  // Example route weather data
  const barData = useMemo(
    () => ({
      labels: ["Route A", "Route B", "Route C", "Route D"],
      series: {
        Temp: [24, 22, 26, 23],
        Precip: [20, 45, 15, 30],
        Sunlight: [7, 5, 9, 6],
      },
    }),
    []
  );

  // Example donut chart for weather composition
  const weatherBreakdown = useMemo(
    () => [
      { name: "Sunny", value: 40 },
      { name: "Cloudy", value: 30 },
      { name: "Rainy", value: 20 },
      { name: "Storm", value: 10 },
    ],
    []
  );

  return (
    <div className="min-h-screen bg-[#F4F2F8] text-slate-800">
      {/* HEADER */}
      <header className="sticky top-0 z-20 bg-white/80 backdrop-blur border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              className="md:hidden inline-flex items-center justify-center rounded-xl border border-slate-200 px-3 py-2"
              onClick={() => setSidebarOpen((p) => !p)}
              aria-label="Toggle sidebar"
            >
              ☰
            </button>
            <div className="flex items-center gap-2">
              <span className="inline-flex h-8 w-8 items-center justify-center rounded-xl bg-blue-600 text-white font-semibold">W</span>
              <span className="font-semibold">Weather Routes</span>
            </div>
          </div>
          <div className="text-sm text-slate-500">Dashboard</div>
        </div>
      </header>

      {/* MAIN CONTENT */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 grid grid-cols-1 md:grid-cols-[240px,1fr] gap-6">
        
        {/* SIDEBAR */}
        <aside className={(sidebarOpen ? "block" : "hidden") + " md:block"}>
          <nav className="sticky top-20 space-y-2">
            <UserCard />
            <SideLink label="Dashboard" active />
            <SideLink label="Routes" />
            <SideLink label="Weather" />
            <SideLink label="Car Data" />
            <SideLink label="Documentation" />
          </nav>
        </aside>

        {/* MAIN PANEL */}
        <main>
          <div className="flex items-center gap-2 mb-4">
            <span className="inline-flex h-8 w-8 items-center justify-center rounded-xl bg-blue-600 text-white">🌍</span>
            <h1 className="text-xl font-semibold">Weather & Routes Dashboard</h1>
          </div>

          {/* STATS CARDS */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
            {stats.map((s) => (
              <div key={s.title} className={`rounded-2xl p-5 text-white shadow-sm bg-gradient-to-tr ${s.gradient}`}>
                <div className="text-sm/5 opacity-90">{s.title}</div>
                <div className="mt-3 text-3xl font-bold tracking-wide">{s.value}</div>
                <div className="mt-2 text-xs/5 opacity-90">
                  {s.change.startsWith("-") ? "Decreased" : "Increased"} by {s.change.replace("+", "").replace("-", "")}
                </div>
              </div>
            ))}
          </div>

          {/* CHARTS */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Bar Chart */}
            <section className="lg:col-span-2 rounded-2xl bg-white p-5 shadow-sm border border-slate-200">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-semibold">Route Weather Comparison</h2>
                <div className="flex items-center gap-3 text-xs">
                  <LegendDot className="bg-yellow-500" label="Temp" />
                  <LegendDot className="bg-sky-500" label="Precip" />
                  <LegendDot className="bg-emerald-500" label="Sunlight" />
                </div>
              </div>
              <BarChart data={barData} />
            </section>

            {/* Donut Chart */}
            <section className="rounded-2xl bg-white p-5 shadow-sm border border-slate-200">
              <h2 className="font-semibold mb-4">Weather Breakdown</h2>
              <DonutChart data={weatherBreakdown} />
              <ul className="mt-6 space-y-2 text-sm">
                {weatherBreakdown.map((t, i) => (
                  <li key={t.name} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className={`inline-block h-3 w-3 rounded-full ${donutColor(i)}`}></span>
                      <span>{t.name}</span>
                    </div>
                    <span className="text-slate-500">{t.value}%</span>
                  </li>
                ))}
              </ul>
            </section>
          </div>
        </main>
      </div>
    </div>
  );
}

/* COMPONENTS */

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
  const max = Math.max(...data.series.Temp, ...data.series.Precip, ...data.series.Sunlight);
  return (
    <div>
      <div className="grid grid-cols-4 gap-4 h-56 items-end">
        {data.labels.map((label, idx) => (
          <div key={label} className="flex flex-col items-center gap-2">
            <div className="flex items-end gap-1 h-full w-full">
              <div className="flex-1 rounded-sm bg-yellow-500/80" style={{ height: `${(data.series.Temp[idx] / max) * 100}%` }} />
              <div className="flex-1 rounded-sm bg-sky-500/80" style={{ height: `${(data.series.Precip[idx] / max) * 100}%` }} />
              <div className="flex-1 rounded-sm bg-emerald-500/80" style={{ height: `${(data.series.Sunlight[idx] / max) * 100}%` }} />
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
  const gradient = `conic-gradient(#facc15 0 ${angles[0]}deg, #60a5fa ${angles[0]}deg ${angles[0] + angles[1]}deg, #34d399 ${angles[0] + angles[1]}deg ${angles[0] + angles[1] + angles[2]}deg, #f87171 ${angles[0] + angles[1] + angles[2]}deg 360deg)`;
  return (
    <div className="flex items-center justify-center">
      <div className="h-48 w-48 rounded-full" style={{ background: gradient, position: "relative" }}>
        <div className="absolute inset-6 bg-white rounded-full grid place-items-center text-slate-600 text-sm">Weather</div>
      </div>
    </div>
  );
}

function donutColor(i) {
  return ["bg-yellow-500", "bg-sky-500", "bg-emerald-500", "bg-red-400"][i] || "bg-slate-400";
}


