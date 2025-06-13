from data_handlers.loader import load_csv
from models.weather import WeatherData


class WeatherDataManager:
    def __init__(self, path):
        self.weather = [WeatherData(**row) for row in load_csv(path)]

    def for_region(self, region):
        return [w for w in self.weather if w.location_id == region]

    def for_date(self, date):
        data = [w for w in self.weather if w.date == date]
        return data

    def stats(self, region):
        data = self.for_region(region)
        if not data:
            return {}
        avg_temp = sum(w.avg_temp for w in data) / len(data)
        sunny_days = len([w for w in data if w.is_sunny()])
        rainy_days = len([w for w in data if w.is_rainy()])
        return {
            "avg_temp": avg_temp,
            "sunny_days": sunny_days,
            "rainy_days": rainy_days
        }

    def get_weather_by_date(self, date_str):
        return [w for w in self.weather if w.date == date_str]
