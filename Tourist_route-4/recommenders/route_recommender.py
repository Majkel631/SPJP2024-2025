class RouteRecommender:
    def __init__(self, routes, weather_data, preferences):
        self.routes = routes
        self.weather_data = weather_data
        self.preferences = preferences

    def recommend(self, date):
        recommendations = []
        weather_by_region = {w.location_id: w for w in self.weather_data if w.date == date}
        for route in self.routes:
            weather = weather_by_region.get(route.region)
            if not weather:
                continue
            if self.preferences.match(route, weather):
                comfort = weather.comfort_index()
                time_est = route.estimated_time()
                categories = route.categorize()
                recommendations.append((route, comfort, time_est, categories))
                if not weather_by_region:
                    print(f"Brak danych pogodowych na dzień {date}. Spróbuj ponownie później.")
                    return []

        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations
