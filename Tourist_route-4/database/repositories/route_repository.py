class RouteRepository:
    def __init__(self, db_manager):
        self.db = db_manager

    def add_route(self, route_data):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO routes (name, region, start_lat, start_lon, end_lat, end_lon,
            length_km, elevation_gain, difficulty, terrain_type, tags, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            route_data['name'], route_data['region'],
            route_data['start_lat'], route_data['start_lon'],
            route_data['end_lat'], route_data['end_lon'],
            route_data['length_km'], route_data['elevation_gain'],
            route_data['difficulty'], route_data['terrain_type'],
            route_data['tags'], route_data['description']
        ))
        conn.commit()

    def find_by_region_and_difficulty(self, region, max_difficulty):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM routes
            WHERE region = ? AND difficulty <= ?
        ''', (region, max_difficulty))
        return cursor.fetchall()