import csv



class MigrationTool:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def migrate_routes_from_csv(self, filepath):
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    cursor.execute('''
                        INSERT INTO routes (name, region, start_lat, start_lon, end_lat, end_lon,
                        length_km, elevation_gain, difficulty, terrain_type, tags, description)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row['name'], row['region'],
                        float(row['start_lat']), float(row['start_lon']),
                        float(row['end_lat']), float(row['end_lon']),
                        float(row.get('length_km', 0)),
                        int(row.get('elevation_gain', 0)),
                        int(row.get('difficulty', 1)),
                        row.get('terrain_type', ''),
                        row.get('tags', ''),
                        row.get('description', '')
                    ))
                except Exception as e:
                    print(f"Błąd migracji trasy: {e}")
        conn.commit()

    def migrate_weather_from_csv(self, filepath):
        region_coords = {
            "Tatry": (49.3, 20.0),
            "Podlasie": (52.8, 23.2),
            "Karpaty": (49.4, 21.5)
        }

        conn = self.db_manager.get_connection()
        cursor = conn.cursor()

        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                region = row["location_id"]
                if region not in region_coords:
                    print(f"Nieznany region: {region}")
                    continue

                lat, lon = region_coords[region]

                try:
                    cursor.execute(
                        """INSERT OR IGNORE INTO weather_data
                        (date, location_lat, location_lon, avg_temp, min_temp, max_temp,
                         precipitation, sunshine_hours, cloud_cover)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            row["date"],
                            lat,
                            lon,
                            float(row["avg_temp"]),
                            float(row["min_temp"]),
                            float(row["max_temp"]),
                            float(row["precipitation"]),
                            float(row["sunshine_hours"]),
                            int(row["cloud_cover"])
                        )
                    )
                except Exception as e:
                    print(f"Błąd importu danych pogodowych (region: {region}, data: {row['date']}): {e}")

        conn.commit()