class UserPreference:
    def __init__(self, max_difficulty, max_length, preferred_temp, max_precipitation):
        self.max_difficulty = int(max_difficulty)
        self.max_length = float(max_length)
        self.preferred_temp = float(preferred_temp)
        self.max_precipitation = float(max_precipitation)

    def match(self, route, weather):
        if route.difficulty > self.max_difficulty:
            return False
        if route.length_km > self.max_length:
            return False
        if weather.avg_temp < self.preferred_temp - 5 or weather.precipitation > self.max_precipitation:
            return False
        return True
