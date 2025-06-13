class WeatherRepository:
    def __init__(self, db_manager):
        self.conn = db_manager.connect()

    def get_weather_by_location_date(self, lat, lon, date):
        cursor = self.conn.execute("""
            SELECT * FROM weather_data
            WHERE location_lat = ? AND location_lon = ? AND date = ?
        """, (lat, lon, date))
        return cursor.fetchone()
