import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional

class DatabaseReports:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def execute_query(self, query: str, params: Tuple = ()):
        self.cursor.execute(query, params)
        return self.cursor

    def most_popular_regions(self) -> List[Tuple[str, int]]:
        self.cursor.execute("""
            SELECT region, COUNT(*) as count
            FROM routes
            GROUP BY region
            ORDER BY count DESC
            LIMIT 5;
        """)
        return self.cursor.fetchall()

    def difficulty_summary(self) -> List[Tuple[int, int]]:
        self.cursor.execute("""
            SELECT difficulty, COUNT(*)
            FROM routes
            GROUP BY difficulty
            ORDER BY difficulty;
        """)
        return self.cursor.fetchall()

    def weather_statistics(self) -> List[Tuple[str, Optional[float], Optional[float], Optional[float], Optional[float]]]:
        cursor = self.execute_query("""
            SELECT name, start_lat, start_lon
            FROM routes
        """)

        statistics = []
        for route_name, lat, lon in cursor.fetchall():
            weather = self.execute_query("""
                SELECT AVG(avg_temp), AVG(precipitation), AVG(sunshine_hours), AVG(cloud_cover)
                FROM weather_data
                WHERE ABS(location_lat - ?) < 0.2 AND ABS(location_lon - ?) < 0.2
            """, (lat, lon))

            result = weather.fetchone()
            if result and any(x is not None for x in result):
                statistics.append((route_name, *result))
            else:
                statistics.append((route_name, None, None, None, None))

        return statistics

    def routes_without_weather(self) -> List[str]:
        self.cursor.execute("""
            SELECT r.name
            FROM routes r
            LEFT JOIN weather_data w
            ON ABS(r.start_lat - w.location_lat) < 0.1
               AND ABS(r.start_lon - w.location_lon) < 0.1
            WHERE w.location_lat IS NULL;
        """)
        return [row[0] for row in self.cursor.fetchall()]

    def add_weather_record(self,
                           location_lat: float,
                           location_lon: float,
                           avg_temp: float,
                           min_temp: float,
                           max_temp: float,
                           precipitation: float,
                           sunshine_hours: float,
                           cloud_cover: int,
                           date: str = None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        try:
            self.cursor.execute("""
                INSERT INTO weather_data 
                (date, location_lat, location_lon, avg_temp, min_temp, max_temp, precipitation, sunshine_hours, cloud_cover)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (date, location_lat, location_lon, avg_temp, min_temp, max_temp, precipitation, sunshine_hours,
                  cloud_cover))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Błąd dodawania rekordu pogodowego: {e}")

    def close(self):
        self.conn.close()
