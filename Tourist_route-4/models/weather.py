class WeatherData:
    def __init__(self, date, location_id, avg_temp, min_temp, max_temp, precipitation, sunshine_hours, cloud_cover):
        self.date = date
        self.location_id = location_id
        self.avg_temp = float(avg_temp)
        self.min_temp = float(min_temp)
        self.max_temp = float(max_temp)
        self.precipitation = float(precipitation)
        self.sunshine_hours = float(sunshine_hours)
        self.cloud_cover = float(cloud_cover)

    def is_sunny(self):
        return self.sunshine_hours >= 6 and self.cloud_cover < 30

    def is_rainy(self):
        return self.precipitation > 1.0

    def comfort_index(self):
        score = 100
        if self.avg_temp < 10 or self.avg_temp > 28:
            score -= 20
        score -= min(self.precipitation * 5, 30)
        score -= min(self.cloud_cover / 2, 20)
        return max(0, min(100, score))
