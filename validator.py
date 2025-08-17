from datetime import datetime

class Validator:
    """
    Validator class to check validity of different sensor data readings.
    Each method returns a dictionary with:
    {
        "valid": True/False,
        "message": "Explanation"
    }
    """

    def validate_temperature(self, temp):
        if not isinstance(temp, (int, float)):
            return {"valid": False, "message": "Temperature must be a number."}
        if temp < -50 or temp > 80:
            return {"valid": False, "message": "Temperature out of realistic range (-50 to 80 °C)."}
        return {"valid": True, "message": "Valid temperature."}

    def validate_humidity(self, humidity):
        if not isinstance(humidity, (int, float)):
            return {"valid": False, "message": "Humidity must be a number."}
        if humidity < 0 or humidity > 100:
            return {"valid": False, "message": "Humidity out of range (0–100%)."}
        return {"valid": True, "message": "Valid humidity."}

    def validate_pressure(self, pressure):
        if not isinstance(pressure, (int, float)):
            return {"valid": False, "message": "Pressure must be a number."}
        if pressure < 300 or pressure > 1100:
            return {"valid": False, "message": "Pressure out of expected range (300–1100 hPa)."}
        return {"valid": True, "message": "Valid pressure."}

    def validate_rainfall(self, rainfall):
        if not isinstance(rainfall, (int, float)):
            return {"valid": False, "message": "Rainfall must be a number."}
        if rainfall < 0:
            return {"valid": False, "message": "Rainfall cannot be negative."}
        return {"valid": True, "message": "Valid rainfall."}

    def validate_gps_coordinates(self, lat, lon):
        if not (isinstance(lat, (int, float)) and isinstance(lon, (int, float))):
            return {"valid": False, "message": "Latitude and longitude must be numbers."}
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return {"valid": False, "message": "GPS coordinates out of range."}
        return {"valid": True, "message": "Valid GPS coordinates."}

    


