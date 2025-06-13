import shutil
import os
import sqlite3
from datetime import datetime, timedelta

class DatabaseAdmin:


    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()


    def get_statistics(self):
        self.cursor.execute("SELECT COUNT(*) FROM routes")
        routes_count = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM weather_data")
        weather_count = self.cursor.fetchone()[0]

        return {
            "routes_count": routes_count,
            "weather_records_count": weather_count
        }

    def check_data_integrity(self):
        self.cursor.execute("""
            SELECT COUNT(*)
            FROM routes r
            LEFT JOIN weather_data w
            ON ABS(r.start_lat - w.location_lat) < 0.1
            AND ABS(r.start_lon - w.location_lon) < 0.1
            WHERE w.id IS NULL
        """)
        missing_weather = self.cursor.fetchone()[0]


        return {
            "routes_without_weather": missing_weather
        }

    def create_backup(self, backup_dir: str):
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"routes_backup_{timestamp}.db")
        self.conn.commit()  # zatwierdź zmiany przed kopiowaniem
        shutil.copy2(self.db_path, backup_path)
        return backup_path

    def clean_old_weather_data(self, days: int = 365):
        """Usuń rekordy pogodowe starsze niż `days` dni, bez daty oraz wszystkie trasy"""
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        # Usuń stare dane pogodowe
        self.cursor.execute(
            "DELETE FROM weather_data WHERE date IS NOT NULL AND date < ?", (cutoff_date,)
        )
        deleted_old = self.cursor.rowcount


        self.cursor.execute(
            "DELETE FROM weather_data WHERE date IS NULL OR TRIM(date) = ''"
        )
        deleted_invalid = self.cursor.rowcount

        # Usuń wszystkie trasy
        self.cursor.execute("DELETE FROM routes")
        deleted_routes = self.cursor.rowcount

        self.conn.commit()

        return {
            "old_weather": deleted_old,
            "invalid_weather": deleted_invalid,
            "routes": deleted_routes,
            "total": deleted_old + deleted_invalid + deleted_routes
        }


    def close(self):
        self.conn.close()

