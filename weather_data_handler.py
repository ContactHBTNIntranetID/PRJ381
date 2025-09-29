import sqlite3
from datetime import datetime

class WeatherDataHandler:
    def __init__(self, db_name='sensor_data.db'):
        self.db_name = db_name
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    temperature REAL,
                    humidity REAL,
                    gas_level REAL,
                    light INTEGER,
                    latitude REAL,
                    longitude REAL,
                    timestamp TEXT
                )
            ''')
            conn.commit()

    def insert_data(self, data):
        required_keys = ['temperature', 'humidity', 'gas_level', 'light', 'latitude', 'longitude']
        if not all(key in data for key in required_keys):
            raise ValueError(f"Missing keys in data. Required: {required_keys}")

        timestamp = data.get('timestamp') or datetime.utcnow().isoformat()

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO readings (temperature, humidity, gas_level, light, latitude, longitude, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['temperature'],
                data['humidity'],
                data['gas_level'],
                data['light'],
                data['latitude'],
                data['longitude'],
                timestamp
            ))
            conn.commit()

    def get_recent_readings(self, limit=10):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM readings ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return cursor.fetchall()

    def clear_all_data(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM readings')
            conn.commit()
