class Route:
    def __init__(
        self,
        id: str = "",
        name: str = "",
        length_km: float = 0.0,
        elevation_gain_m: int = 0,
        time_minutes: int = 0,
        gps_coords=None,
        difficulty: str = "nieznana",
        description: str = "",
        reviews=None,
        warnings=None,  # lista ostrzeżeń
    ):
        self.id = id
        self.name = name
        self.length_km = length_km
        self.elevation_gain_m = elevation_gain_m
        self.time_minutes = time_minutes
        self.gps_coords = gps_coords if gps_coords is not None else []
        self.difficulty = difficulty
        self.description = description
        self.reviews = reviews if reviews is not None else []
        self.rating = 0.0
        self.category = "nieznana"
        self.warnings = warnings if warnings is not None else []
        self.map_path = ""
        self.elevation_profile_path = ""