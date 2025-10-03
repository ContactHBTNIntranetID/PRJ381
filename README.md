# Car Telemetry Module

This module simulates **car telemetry data** (speed, engine temperature, battery level) and displays it in real-time using React.  
It also includes a **live-updating chart** (speed vs. time) built with Recharts.

---

## Features
- Simulated telemetry values:
  - Speed (km/h)
  - Engine Temperature (°C)
  - Battery Level (%)
- Updates every **3 seconds** automatically.
- Rolling history of the **last 10 readings**.
- Line chart showing **speed trend** over time.
- Built with **React Hooks** (`useState`, `useEffect`) and **Recharts**.

---

## Setup & Installation

1. Navigate to your React project root.
2. Install Recharts (if not already installed):

   ```bash
   npm install recharts
3. Create a new component file:
    src/components/CarTelemetry.jsx

Usage

Import the component into your main app or dashboard:

    import CarTelemetry from "./components/CarTelemetry";

        function App() {
            return (
                <div>
                <h1>Route Weather & Telemetry App</h1>
                <CarTelemetry />
                </div>
            );
        }       

export default App;

Run the app:
    npm install recharts
    npm install 
    npm run dev
    npm start