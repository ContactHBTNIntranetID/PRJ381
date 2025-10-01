/**
 * Person 2: Map & Routes Integration
 * - Integrates Mapbox Directions API for fetching driving directions.
 * - Displays interactive map using React-Leaflet.
 * - Adds markers for start and end locations.
 * - Renders alternative routes with different colors.
 * - Ensures correct parsing of GeoJSON coordinates ([lng, lat] to [lat, lng]).
 */

import React, { useState, useEffect, useCallback } from 'react';
import { MapContainer, TileLayer, Polyline, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const MapRoutes = ({ start, end }) => {
  const [routeList, setRouteList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mapInstance, setMapInstance] = useState(null);

  // Get Mapbox access token from environment
  const MAPBOX_ACCESS_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN;

  // Validate coordinate format
  const isValidCoord = (coord) =>
    coord &&
    typeof coord.lat === 'number' &&
    typeof coord.lng === 'number' &&
    coord.lat >= -90 && coord.lat <= 90 &&
    coord.lng >= -180 && coord.lng <= 180;

  // Fetch routes from Mapbox Directions API
  const fetchRoutes = useCallback(async () => {
    if (!MAPBOX_ACCESS_TOKEN) {
      setError('Mapbox access token is missing. Set REACT_APP_MAPBOX_TOKEN in .env');
      return;
    }

    if (!isValidCoord(start) || !isValidCoord(end)) {
      setError('Invalid start or end coordinates');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Mapbox expects: lng,lat;lng,lat
      const coords = `${start.lng},${start.lat};${end.lng},${end.lat}`;
      const url = `https://api.mapbox.com/directions/v5/mapbox/driving/${coords}` +
        `?alternatives=true&geometries=geojson&access_token=${MAPBOX_ACCESS_TOKEN}`;

      const response = await fetch(url);

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.message || `HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      if (data.code !== 'Ok' || !data.routes || data.routes.length === 0) {
        throw new Error('No routes found. Try different locations.');
      }

      // Ensure correct parsing of GeoJSON coordinates ([lng, lat] to [lat, lng])
      const parsedRoutes = data.routes.map((route, idx) => ({
        id: idx,
        geometry: route.geometry,
        distance: route.distance, // meters
        duration: route.duration, // seconds
      }));

      setRouteList(parsedRoutes);

      // Auto-fit map bounds to start/end
      if (mapInstance) {
        const bounds = L.latLngBounds([
          [start.lat, start.lng],
          [end.lat, end.lng]
        ]);
        mapInstance.fitBounds(bounds, { padding: [60, 60] });
      }
    } catch (err) {
      console.error('Route fetch error:', err);
      setError(err.message || 'Failed to load routes');
    } finally {
      setLoading(false);
    }
  }, [start, end, mapInstance, MAPBOX_ACCESS_TOKEN]);

  // Debounced route fetch
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchRoutes();
    }, 400);
    return () => clearTimeout(timer);
  }, [fetchRoutes]);

  // Route color palette
  const routeColors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6'];

  return (
    <div style={{ height: '100vh', width: '100%', position: 'relative' }}>
      <MapContainer
        center={start && isValidCoord(start) ? [start.lat, start.lng] : [0, 0]}
        zoom={start ? 10 : 1}
        style={{ height: '100%', width: '100%' }}
        whenCreated={setMapInstance}
        zoomControl={true}
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='© <a href="https://www.mapbox.com/about/maps/">Mapbox</a>'
          url={`https://api.mapbox.com/styles/v1/mapbox/streets-v12/tiles/{z}/{x}/{y}?access_token=${MAPBOX_ACCESS_TOKEN}`}
        />

        {/* Start Marker */}
        {start && isValidCoord(start) && (
          <Marker position={[start.lat, start.lng]}>
            <Popup><b>Start</b></Popup>
          </Marker>
        )}

        {/* End Marker */}
        {end && isValidCoord(end) && (
          <Marker position={[end.lat, end.lng]}>
            <Popup><b>Destination</b></Popup>
          </Marker>
        )}

        {/* Render Alternative Routes with Different Colors */}
        {routeList.map((route) => (
          !!route.geometry && (
            <Polyline
              key={route.id}
              positions={route.geometry.coordinates.map(([lng, lat]) => [lat, lng])}
              color={routeColors[route.id % routeColors.length]}
              weight={route.id === 0 ? 7 : 5}
              opacity={0.9}
            />
          )
        ))}
      </MapContainer>

      {/* Loading Indicator */}
      {loading && (
        <div className="map-overlay" style={{
          top: '10px',
          left: '50%',
          transform: 'translateX(-50%)',
          background: 'rgba(255,255,255,0.9)',
          padding: '10px 20px',
          borderRadius: '8px',
          fontWeight: 'bold'
        }}>
          Calculating routes...
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="map-overlay" style={{
          top: '10px',
          left: '50%',
          transform: 'translateX(-50%)',
          background: 'rgba(255,230,230,0.95)',
          color: '#d32f2f',
          padding: '10px 20px',
          borderRadius: '8px',
          maxWidth: '80%',
          textAlign: 'center'
        }}>
          {error}
        </div>
      )}

      {/* Route Info Panel */}
      {routeList.length > 0 && (
        <div className="map-overlay" style={{
          top: '10px',
          right: '10px',
          background: 'rgba(255,255,255,0.95)',
          padding: '12px',
          borderRadius: '8px',
          fontSize: '14px',
          maxHeight: '300px',
          overflowY: 'auto'
        }}>
          <h4 style={{ margin: '0 0 10px 0', fontSize: '16px' }}>Route Options</h4>
          {routeList.map((route, i) => (
            <div key={i} style={{ 
              color: routeColors[i % routeColors.length], 
              marginBottom: '6px',
              fontWeight: i === 0 ? 'bold' : 'normal'
            }}>
              <span style={{ marginRight: '8px' }}>●</span>
              Route {i + 1}: {(route.duration / 60).toFixed(0)} min, {(route.distance / 1000).toFixed(1)} km
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MapRoutes;