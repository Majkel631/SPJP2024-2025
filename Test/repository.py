import csv
from models import Route
from exceptions import DataParsingError

class FileRouteRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_all(self):
        routes = []
        try:
            with open(self.file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        route = Route(
                            id=row['id'],
                            name=row['name'],
                            region=row['region'],
                            start_lat=row['start_lat'],
                            start_lon=row['start_lon'],
                            end_lat=row['end_lat'],
                            end_lon=row['end_lon'],
                            length_km=row['length_km'],
                            elevation_gain=row['elevation_gain'],
                            difficulty=row['difficulty'],
                            terrain_type=row['terrain_type'],
                            tags=row['tags']
                        )
                        routes.append(route)
                    except (ValueError, KeyError) as e:
                        raise DataParsingError(f"Invalid row data: {row}") from e
        except FileNotFoundError:
            raise
        return routes