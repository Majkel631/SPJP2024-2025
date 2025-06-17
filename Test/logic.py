class RouteRecommender:
    def __init__(self, repository):
        self.repository = repository

    def recommend(self, preference):
        all_routes = self.repository.get_all()
        return [
            route for route in all_routes
            if route.difficulty <= preference.max_difficulty and route.terrain_type == preference.terrain
        ]