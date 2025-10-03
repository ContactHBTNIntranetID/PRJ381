import React, { useMemo, useState } from "react";
import CarTelemetry from "./components/CarTelemetry";

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const stats = [
    { title: "Temperature", value: "24°C", change: "+2°C", gradient: "from-yellow-400 to-orange-500" },
    { title: "Precipitation", value: "20%", change: "-5%", gradient: "from-sky-400 to-blue-600" },
    { title: "Air Quality", value: "Good (45 AQI)", change: "+3%", gradient: "from-emerald-400 to-teal-500" },
  ];

  const barData = useMemo(
    () => ({
      labels: ["Route 1", "Route 2", "Route 3", "Route 4", "Route 5", "Route 6", "Route 7", "Route 8"],
      series: {
        temp: ["12°C", "25°C", "18°C", "30°C", "22°C", "28°C", "16°C", "24°C"],
        precip: [20, 10, 14, 18, 26, 12, 22, 10],
        sunlight: [8, 14, 10, 12, 16, 20, 10, 18],
      },
    }),
    []
  );

  const traffic = useMemo(
    () => [
      { name: "Search Engines", value: 30 },
      { name: "Direct Click", value: 30 },
      { name: "Bookmarks", value: 40 },
    ],
    []
  );

  return (
    <div className="min-h-screen bg-[#F4F2F8] text-slate-800">
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
              <span className="inline-flex h-8 w-8 items-center justify-center rounded-xl bg-violet-600 text-white font-semibold">W</span>
              <span className="font-semibold">Weather Routes</span>
            </div>
          </div>
          <div className="text-sm text-slate-500">Dashboard</div>
        </div>
      </header>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 grid grid-cols-1 md:grid-cols-[240px,1fr] gap-6">
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
        <main>
          <div className="flex items-center gap-2 mb-4">
            <span className="inline-flex h-8 w-8 items-center justify-center rounded-xl bg-violet-600 text-white">🏠</span>
            <h1 className="text-xl font-semibold">Dashboard</h1>
          </div>
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
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <section className="lg:col-span-2 rounded-2xl bg-white p-5 shadow-sm border border-slate-200">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-semibold">Weather and Routes</h2>
                <div className="flex items-center gap-3 text-xs">
                  <LegendDot className="bg-violet-500" label="Temperature" />
                  <LegendDot className="bg-pink-400" label="Precipitation" />
                  <LegendDot className="bg-sky-500" label="Sunlight" />
                </div>
              </div>
              <BarChart data={barData} />
            </section>
            <section className="rounded-2xl bg-white p-5 shadow-sm border border-slate-200">
              <h2 className="font-semibold mb-4">Traffic Sources</h2>
              <DonutChart data={traffic} />
              <ul className="mt-6 space-y-2 text-sm">
                {traffic.map((t, i) => (
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
          {/* Car Telemetry + Weather Dashboard Integration */}
          <div className="mt-10">
            <CarTelemetry />
          </div>
        </main>
      </div>
    </div>
  );
}

function UserCard() {
  return (
    <div className="rounded-2xl bg-white p-4 shadow-sm border border-slate-200 mb-2 flex items-center gap-3">
      <div className="h-12 w-12 rounded-full bg-gradient-to-tr from-violet-500 to-fuchsia-500 text-white flex items-center justify-center font-semibold">
        D
      </div>
      <div>
        <div className="font-medium">David Grey. H</div>
        <div className="text-xs text-slate-500">Project Manager</div>
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
          ? "bg-violet-50 border-violet-200 text-violet-700"
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
  const max = Math.max(...data.series.temp, ...data.series.precip, ...data.series.sunlight);
  return (
    <div>
      <div className="grid grid-cols-8 gap-4 h-56 items-end">
        {data.labels.map((label, idx) => (
          <div key={label} className="flex flex-col items-center gap-2">
            <div className="flex items-end gap-1 h-full w-full">
              <div className="flex-1 rounded-sm bg-violet-500/80" style={{ height: `${(data.series.temp[idx] / max) * 100}%` }} />
              <div className="flex-1 rounded-sm bg-pink-400/80" style={{ height: `${(data.series.precip[idx] / max) * 100}%` }} />
              <div className="flex-1 rounded-sm bg-sky-500/80" style={{ height: `${(data.series.sunlight[idx] / max) * 100}%` }} />
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
  const gradient = `conic-gradient(#8b5cf6 0 ${angles[0]}deg, #f472b6 ${angles[0]}deg ${angles[0] + angles[1]}deg, #0ea5e9 ${angles[0] + angles[1]}deg 360deg)`;
  return (
    <div className="flex items-center justify-center">
      <div className="h-48 w-48 rounded-full" style={{ background: gradient, position: "relative" }}>
        <div className="absolute inset-6 bg-white rounded-full grid place-items-center text-slate-600 text-sm">Traffic</div>
      </div>
    </div>
  );
}

function donutColor(i) {
  return ["bg-violet-500", "bg-pink-400", "bg-sky-500"][i] || "bg-slate-400";
}