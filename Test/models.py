class Route:
    def __init__(self, id, name, region, start_lat, start_lon, end_lat, end_lon,
                 length_km, elevation_gain, difficulty, terrain_type, tags):
        if float(length_km) < 0:
            raise ValueError("Length cannot be negative")
        if int(difficulty) < 1 or int(difficulty) > 5:
            raise ValueError("Difficulty must be between 1 and 5")

        self.id = int(id)
        self.name = name
        self.region = region
        self.start_lat = float(start_lat)
        self.start_lon = float(start_lon)
        self.end_lat = float(end_lat)
        self.end_lon = float(end_lon)
        self.length_km = float(length_km)
        self.elevation_gain = int(elevation_gain)
        self.difficulty = int(difficulty)
        self.terrain_type = terrain_type
        self.tags = [tag.strip() for tag in tags.split(',') if tag.strip()]

class UserPreference:
    def __init__(self, max_difficulty: int, terrain: str):
        if max_difficulty < 1 or max_difficulty > 5:
            raise ValueError("Invalid difficulty preference")
        self.max_difficulty = max_difficulty
        self.terrain = terrain