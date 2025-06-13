import re
from typing import List, Tuple

class TextProcessor:
    TIME_PATTERN = re.compile(
        r'(?:(\d+(?:[.,]\d+)?)\s*h(?:od(?:zin(?:y)?)?)?)?\s*'
        r'(?:(\d+)\s*min(?:ut(?:y)?)?)?'
    )
    LANDMARKS = ['schronisko', 'szczyt', 'przełęcz', 'jezioro', 'punkt widokowy']
    WARNINGS = ['niebezpieczne', 'zalecane kaski', 'uwaga', 'trudne warunki', 'śliskie']

    COORD_PATTERN = re.compile(
        r'(\d{1,2})[°º]?\s*(\d{1,2})?[\'’′]?\s*(\d{1,2}(?:\.\d+)?)?"?\s*([NSEW])'
    )

    def extract_time(self, text: str) -> float:
        text = text.lower().replace(',', '.')
        match = self.TIME_PATTERN.search(text)
        if not match:
            return 0.0
        hours = float(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        return hours * 60 + minutes

    def identify_landmarks(self, text: str) -> List[str]:
        text = text.lower()
        return [lm for lm in self.LANDMARKS if lm in text]

    def identify_warnings(self, text: str) -> List[str]:
        text = text.lower()
        return [warn for warn in self.WARNINGS if warn in text]

    def standardize_coordinates(self, text: str) -> List[Tuple[float, float]]:
        coords = []
        matches = list(self.COORD_PATTERN.finditer(text))
        i = 0
        while i + 1 < len(matches):
            lat = self.dms_to_decimal(matches[i].groups())
            lon = self.dms_to_decimal(matches[i + 1].groups())
            coords.append((lat, lon))
            i += 2
        return coords

    def dms_to_decimal(self, groups: Tuple[str, str, str, str]) -> float:
        degrees = int(groups[0])
        minutes = int(groups[1]) if groups[1] else 0
        seconds = float(groups[2]) if groups[2] else 0.0
        direction = groups[3]
        decimal = degrees + minutes / 60 + seconds / 3600
        if direction in ['S', 'W']:
            decimal = -decimal
        return decimal

    def extract_info(self, text: str) -> dict:
        time_minutes = self.extract_time(text)
        warnings = self.identify_warnings(text)
        difficulty = None
        text_lower = text.lower()
        if "łatwa" in text_lower:
            difficulty = "łatwa"
        elif "średnia" in text_lower:
            difficulty = "średnia"
        elif "trudna" in text_lower:
            difficulty = "trudna"
        return {
            "time_minutes": time_minutes,
            "warnings": warnings,
            "difficulty": difficulty
        }

    def process(self, route):
        text = route.description.lower()
        route.time_estimates = [self.extract_time(text)]
        route.landmarks = self.identify_landmarks(text)
        route.warnings = self.identify_warnings(text)
        route.coordinates = self.standardize_coordinates(route.description)


class Route:
    def __init__(self, name: str, description: str = "", length_km: float = 0.0,
                 time_minutes: int = 0, elevation_gain_m: int = 0,
                 difficulty: str = None, id: str = None):
        self.name = name
        self.description = description
        self.length_km = length_km
        self.time_minutes = time_minutes
        self.elevation_gain_m = elevation_gain_m
        self.difficulty = difficulty
        self.id = id
        self.warnings = []
        self.landmarks = []
        self.time_estimates = []
        self.coordinates = []
        self.category = None
        self.rating = None
        self.map_path = None
        self.elevation_profile_path = None
