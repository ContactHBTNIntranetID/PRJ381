class Validator:
    """
    Validator class to check validity of different sensor data readings.
    Each method returns True if data is valid, False otherwise.
    """

    def validate_temperature(self, temp):
        """
        Validate temperature:
        - Must be int or float
        - Must be within realistic range (-50 to 80 °C)
        """
        if not isinstance(temp, (int, float)):
            return False
        if temp < -50 or temp > 80:
            return False
        return True

    def validate_humidity(self, humidity):
        """
        Validate humidity:
        - Must be int or float
        - Must be within range 0 to 100 (%)
        """
        if not isinstance(humidity, (int, float)):
            return False
        if humidity < 0 or humidity > 100:
            return False
        return True

    def validate_pressure(self, pressure):
        """
        Validate barometric pressure:
        - Must be int or float
        - Must be within expected atmospheric range (e.g., 300 to 1100 hPa)
        """
        if not isinstance(pressure, (int, float)):
            return False
        if pressure < 300 or pressure > 1100:
            return False
        return True

    def validate_rainfall(self, rainfall):
        """
        Validate rainfall sensor reading:
        - Must be int or float
        - Must be >= 0 (no negative rainfall)
        """
        if not isinstance(rainfall, (int, float)):
            return False
        if rainfall < 0:
            return False
        return True

    def validate_gps_coordinates(self, lat, lon):
        """
        Validate GPS coordinates:
        - Latitude must be float between -90 and 90
        - Longitude must be float between -180 and 180
        """
        if not (isinstance(lat, (int, float)) and isinstance(lon, (int, float))):
            return False
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return False
        return True

    
