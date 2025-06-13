import sqlite3
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def initialize_database(self):
        self.connect()
        with open('sql/schema.sql', 'r') as schema_file:
            schema = schema_file.read()
        self.connection.executescript(schema)
        self.connection.commit()

    def get_connection(self):
        if not self.connection:
            self.connect()
        return self.connection

    def add_weather_record(self, weather_data: dict, source='manual'):
        if not self.connection:
            self.connect()
        self.cursor.execute("""
            INSERT OR REPLACE INTO weather_data 
            (date, location_lat, location_lon, avg_temp, min_temp, max_temp, precipitation, sunshine_hours, cloud_cover, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            weather_data['date'],
            weather_data['location_lat'],
            weather_data['location_lon'],
            weather_data['avg_temp'],
            weather_data['min_temp'],
            weather_data['max_temp'],
            weather_data['precipitation'],
            weather_data['sunshine_hours'],
            weather_data['cloud_cover'],
            source
        ))
        self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None