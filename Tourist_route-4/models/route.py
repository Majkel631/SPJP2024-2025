class Route:
    def __init__(self, id, name, region, start_lat, start_lon, end_lat, end_lon, length_km, elevation_gain, difficulty, terrain_type, tags):
        self.id = int(id)
        self.name = name
        self.region = region
        self.start_lat = float(start_lat)
        self.start_lon = float(start_lon)
        self.end_lat = float(end_lat)
        self.end_lon = float(end_lon)
        self.length_km = float(length_km)
        self.elevation_gain = float(elevation_gain)
        self.difficulty = int(difficulty)
        self.terrain_type = terrain_type
        self.tags = tags.split(',') if tags else []

    def midpoint(self):
        lat = (self.start_lat + self.end_lat) / 2
        lon = (self.start_lon + self.end_lon) / 2
        return lat, lon

    def estimated_time(self):
        terrain_factor = {
            'mountain': 1.5,
            'forest': 1.2,
            'lakeside': 1.0,
            'urban': 1.0
        }.get(self.terrain_type, 1.0)

        difficulty_multiplier = 1 + (self.difficulty - 1) * 0.2
        time = self.length_km / 4  # base speed: 4 km/h
        time += self.elevation_gain / 600  # +1h per 600m up
        return time * difficulty_multiplier * terrain_factor

    def categorize(self):
        categories = []
        if self.difficulty <= 2 and self.length_km <= 10:
            categories.append("Rodzinna")
        if "view" in self.tags or "panorama" in self.tags:
            categories.append("Widokowa")
        if self.difficulty >= 4:
            categories.append("Ekstremalna")
        if self.length_km >= 15:
            categories.append("Sportowa")
        return categories
