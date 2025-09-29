## **CampusLearn Route & Weather Planner** 🗺️

### **1. Project Overview**

This application is a real-time route and weather planner built using **React** and the **Vite** build tool. It integrates mapping, directions, and weather APIs to help users plan their travel, and includes a core feature for monitoring simulated car telemetry data.

-----

### **2. Core Features**

  * **Route Planning:** Display optimal driving routes between two user-defined locations (utilizing the **Mapbox Directions API**).
  * **Weather Integration:** Fetches and displays real-time weather data (temperature, humidity, wind speed) for the destination (utilizing the **OpenWeather API**).
  * **Car Telemetry Module:** This module simulates and displays **car telemetry data** (speed, engine temperature, battery level) in real-time.
      * Simulated values: Speed (km/h), Engine Temperature (°C), Battery Level (%).
      * Updates every **3 seconds** automatically with a rolling history of the **last 10 readings**.
      * Includes a live-updating line chart showing the **speed trend** over time, built with **Recharts**.
  * **User Interface:** Built with React, uses Hot Module Reloading (HMR) for fast development, and is responsive for desktop and mobile use.

-----

### **3. Getting Started**

#### **Prerequisites**

  * **Node.js** (LTS version recommended)
  * **npm** (Node Package Manager)

#### **Installation**

1.  **Clone the repository:**
    ```bash
    git clone [Your Repository URL]
    cd route-weather-app
    ```
2.  **Install all project dependencies:**
    ```bash
    npm install
    ```
3.  **Install the charting library:** (Required for the Telemetry Module)
    ```bash
    npm install recharts
    ```

#### **Environment Variables (API Keys)**

This project requires API access. Create a file named **`.env`** in the root directory. **Vite requires variables exposed to the frontend to be prefixed with `VITE_`**.

| Variable Name | Purpose |
| :--- | :--- |
| `VITE_MAPBOX_TOKEN` | Your Mapbox API access token for maps and directions. |
| `VITE_OPENWEATHER_KEY` | Your OpenWeather API key for fetching weather data. |

-----

### **4. Available Scripts**

| Command | Action | Notes |
| :--- | :--- | :--- |
| `npm run dev` | Starts the local development server. | Uses HMR for Fast Refresh, powered by Babel or SWC plugins. |
| `npm run build` | **Compiles the app** for production. | Creates the optimized static file folder: **`/dist`**. |
| `npm run lint` | Runs the ESLint configuration. | Checks code for errors and style inconsistencies. |

#### **Extending the ESLint configuration**

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://www.google.com/search?q=%5Bhttps://typescript-eslint.io%5D\(https://typescript-eslint.io\)) in your project.

-----

### **5. Deployment Strategy (Person 6 Deliverable)**

The application utilizes a Continuous Deployment (CD) pipeline to automatically build and publish the application.

#### **Configuration Summary:**

  * **Platform:** Netlify / Vercel (or similar CI/CD service).
  * **Build Tool:** Vite
  * **Build Command:** `npm run build`
  * **Publish Directory:** **`dist`**

#### **Deployment Checklist:**

1.  **Secure API Keys:** The `VITE_MAPBOX_TOKEN` and `VITE_OPENWEATHER_KEY` are securely stored in the deployment platform's **Environment Variables** dashboard to protect them from public exposure.
2.  **Single-Page Application (SPA) Fallback:** A redirect rule is configured on the hosting platform (e.g., using a `_redirects` file or Vercel configuration) to ensure all application URLs are served by the main `index.html` file, allowing the React Router to handle client-side navigation.
