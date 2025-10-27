import React, { useState, useRef, useMemo } from 'react';
import Map, { Marker, Source, Layer, Popup } from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import mapboxgl from 'mapbox-gl'; // Import for LngLatBounds

// Get the token securely from the .env file
const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN;

const routeColors = ['#007bff', '#dc3545', '#28a745', '#ffc107'];

// Layer style for the route lines
const routeLayerStyle = {
  id: 'route-line',
  type: 'line',
  layout: {
    'line-join': 'round',
    'line-cap': 'round'
  },
  paint: {} // Paint properties are set dynamically
};

/**
 * A React component to display a Mapbox map with route finding.
 */
function MapboxMap() {
  // State for the map's viewport
  const [viewState, setViewState] = useState({
    longitude: 28.229,  // Pretoria Lng
    latitude: -25.747, // Pretoria Lat
    zoom: 12
  });

  // State to hold the user's text input
  const [startAddress, setStartAddress] = useState('');
  const [endAddress, setEndAddress] = useState('');

  // State to hold the coordinates [lng, lat]
  const [startPoint, setStartPoint] = useState(null);
  const [endPoint, setEndPoint] = useState(null);

  // State to hold the GeoJSON data for all routes
  const [routesGeoJSON, setRoutesGeoJSON] = useState(null);

  // A ref to the map instance for fitting bounds
  const mapRef = useRef();

  /**
   * Fetches coordinates for a given address string using Mapbox Geocoding.
   */
  const geocode = async (address) => {
    // Uses the secure MAPBOX_TOKEN from the .env file
    const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(address)}.json?access_token=${MAPBOX_TOKEN}&limit=1`;
    try {
      const response = await fetch(url);
      const data = await response.json();
      if (data.features.length > 0) {
        return data.features[0].center; // Returns [lng, lat]
      } else {
        alert(`Could not find location: ${address}`);
        return null;
      }
    } catch (error) {
      console.error(`Geocoding error for ${address}:`, error);
      return null;
    }
  };

  /**
   * Fetches directions from Mapbox and updates the map.
   */
  const handleGetRoute = async () => {
    if (!startAddress || !endAddress) {
      alert("Please enter both a start and end location.");
      return;
    }
    
    // Clear old data
    setStartPoint(null);
    setEndPoint(null);
    setRoutesGeoJSON(null);

    try {
      // 1. Geocode addresses
      const start = await geocode(startAddress);
      const end = await geocode(endAddress);
      if (!start || !end) return;

      // Update state with new markers
      setStartPoint(start);
      setEndPoint(end);

      // 2. Fetch routes
      const coordsString = `${start.join(',')};${end.join(',')}`;
      const url = `https://api.mapbox.com/directions/v5/mapbox/driving/${coordsString}?alternatives=true&geometries=geojson&access_token=${MAPBOX_TOKEN}`;
      
      const response = await fetch(url);
      const data = await response.json();
      if (!data.routes || data.routes.length === 0) throw new Error("No routes found.");
      
      // 3. Format route data as a GeoJSON FeatureCollection
      const features = data.routes.map((route, index) => ({
        type: 'Feature',
        geometry: route.geometry,
        properties: {
          routeIndex: index,
          color: routeColors[index % routeColors.length],
          isMainRoute: index === 0
        }
      }));

      setRoutesGeoJSON({ type: 'FeatureCollection', features });

      // 4. Fit map to the main route's bounds
      const mainRouteGeometry = data.routes[0].geometry.coordinates;
      const bounds = new mapboxgl.LngLatBounds(mainRouteGeometry[0], mainRouteGeometry[0]);
      for (const coord of mainRouteGeometry) {
        bounds.extend(coord);
      }
      mapRef.current?.fitBounds(bounds, { padding: 50, duration: 1000 });

    } catch (error) {
      console.error("Error getting route:", error);
      alert("Could not find a route. Please check your locations.");
    }
  };
  
  // Memoize the map layers to prevent re-renders
  const routeLayers = useMemo(() => {
    if (!routesGeoJSON) return null;

    return routesGeoJSON.features.map((feature) => (
      <Layer
        key={feature.properties.routeIndex}
        {...routeLayerStyle}
        id={`route-${feature.properties.routeIndex}`}
        paint={{
          'line-color': feature.properties.color,
          'line-width': feature.properties.isMainRoute ? 7 : 5,
          'line-opacity': feature.properties.isMainRoute ? 1.0 : 0.8
        }}
        filter={['==', 'routeIndex', feature.properties.routeIndex]}
      />
    ));
  }, [routesGeoJSON]);

  // This is the HTML-like (JSX) structure that React will render
  return (
    <div className="space-y-4">
      {/* 1. Input Form (Styled with Tailwind) */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <input
          type="text"
          placeholder="Start location"
          value={startAddress}
          onChange={(e) => setStartAddress(e.target.value)}
          className="md:col-span-2 w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-violet-500 focus:border-violet-500"
        />
        <input
          type="text"
          placeholder="End location"
          value={endAddress}
          onChange={(e) => setEndAddress(e.target.value)}
          className="md:col-span-2 w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-violet-500 focus:border-violet-500"
        />
        <button
          onClick={handleGetRoute}
          className="md:col-span-1 w-full px-3 py-2 bg-violet-600 text-white rounded-md shadow-sm hover:bg-violet-700 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2"
        >
          Get Route
        </button>
      </div>

      {/* 2. The Map Container */}
      <div className="w-full h-[500px] rounded-lg overflow-hidden border border-slate-200 shadow-sm">
        <Map
          ref={mapRef}
          {...viewState}
          onMove={evt => setViewState(evt.viewState)}
          mapboxAccessToken={MAPBOX_TOKEN} // Token is passed to the Map component here
          mapStyle="mapbox://styles/mapbox/streets-v12"
        >
          {/* Add Markers */}
          {startPoint && (
            <Marker longitude={startPoint[0]} latitude={startPoint[1]} color="blue">
              <Popup>Start Location</Popup>
            </Marker>
          )}
          {endPoint && (
            <Marker longitude={endPoint[0]} latitude={endPoint[1]} color="red">
              <Popup>End Location</Popup>
            </Marker>
          )}

          {/* Add Route Lines */}
          {routesGeoJSON && (
            <Source type="geojson" data={routesGeoJSON}>
              {routeLayers}
            </Source>
          )}
        </Map>
      </div>
    </div>
  );
}

export default MapboxMap;
