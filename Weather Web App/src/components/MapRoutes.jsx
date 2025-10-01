import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function MapRoutes() {
  return (
    <div style={{ height: "400px", width: "100%", marginBottom: "20px" }}>
      <MapContainer
        center={[-25.7479, 28.2293]} // Pretoria
        zoom={13}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        />

        <Marker position={[-25.7479, 28.2293]}>
          <Popup>Pretoria!</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}