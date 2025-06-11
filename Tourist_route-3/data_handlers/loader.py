from typing import List, Dict
from extractors.html_route_extractor import HTMLRouteExtractor, HTMLWeatherExtractor

def load_routes_from_html(path: str) -> List[Dict]:
    with open(path, encoding='utf-8') as f:
        html = f.read()

    extractor = HTMLRouteExtractor()
    routes = extractor.parse_html(html)

    if isinstance(routes, dict):
        return [routes]
    return routes


def load_weather_from_html(path: str) -> List[Dict]:
    with open(path, encoding='utf-8') as f:
        html = f.read()

    extractor = HTMLWeatherExtractor()
    weather = extractor.parse_html(html)

    if isinstance(weather, dict):
        return [weather]
    return weather