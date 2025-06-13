from models.route import Route


class RouteDataManager:
    def __init__(self, path):
        from data_handlers.loader import load_csv
        self.routes = [Route(**row) for row in load_csv(path)]

    def filter_by_region(self, region):
        return [r for r in self.routes if r.region == region]
