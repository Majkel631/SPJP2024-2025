from data_handlers.route_manager import RouteDataManager
from data_handlers.weather_manager import WeatherDataManager
from models.preferences import UserPreference
from recommenders.route_recommender import RouteRecommender
from ui.user_interface import UserInterface

if __name__ == "__main__":
    user_date = input("Podaj datę (YYYY-MM-DD): ").strip()

    route_mgr = RouteDataManager("data/routes/routes.csv")
    weather_mgr = WeatherDataManager("data/weather/weather.csv")

    weather_for_day = weather_mgr.get_weather_by_date(user_date)
    if not weather_for_day:
        print(f"Brak danych pogodowych dla daty: {user_date}")
        exit()

    prefs_raw = UserInterface.get_preferences()
    preferences = UserPreference(**prefs_raw)

    recommender = RouteRecommender(route_mgr.routes, weather_mgr.weather, preferences)
    results = recommender.recommend(user_date)

    UserInterface.show_recommendations(results, user_date)
    results = recommender.recommend(user_date)

    if not results:
        print(f"Brak pasujących tras dla daty {user_date} z pożądanymi prefernacjami ")
    else:
        UserInterface.show_recommendations(results, user_date)