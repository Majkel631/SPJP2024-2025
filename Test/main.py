from repository import FileRouteRepository
from logic import RouteRecommender
from models import UserPreference

def main():
    repo = FileRouteRepository('routes.csv')
    recommender = RouteRecommender(repo)
    preference = UserPreference(max_difficulty=3, terrain='mountain')
    recommended = recommender.recommend(preference)
    for route in recommended:
        print(f"{route.name}: {route.length_km}km, difficulty {route.difficulty}, terrain {route.terrain_type}, tags {route.tags}")


if __name__ == '__main__':
    main()