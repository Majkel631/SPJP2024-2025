import os
import re
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

class WebDataCollector:
    def fetch_and_cache(self, url: str, cache_dir: str) -> str:
        os.makedirs(cache_dir, exist_ok=True)
        filename = url.split("/")[-1] + ".html"
        filepath = os.path.join(cache_dir, filename)

        if not os.path.exists(filepath):
            response = requests.get(url)
            if response.status_code == 200:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(response.text)
            else:
                raise Exception(f"Błąd pobierania: {response.status_code}")
        return filepath

class HTMLRouteExtractor:
    def parse_html(self, html: str) -> List[Dict]:
        soup = BeautifulSoup(html, 'html.parser')
        routes = []

        route_divs = soup.find_all('div')

        for div in route_divs:
            h2 = div.find('h2')
            if not h2:
                continue
            route_name = h2.get_text(strip=True)

            route_info = {
                'name': route_name,
                'reviews': [],
                'warnings': []
            }

            for p in div.find_all('p'):
                strong = p.find('strong')
                if strong:
                    key = strong.get_text(strip=True).rstrip(':')
                    val = p.get_text(strip=True).replace(strong.get_text(), '').strip()

                    if key == "ID":
                        route_info['id'] = val
                    elif key == "Długość":
                        try:
                            route_info['length_km'] = float(val.replace('km', '').strip())
                        except ValueError:
                            route_info['length_km'] = 0.0
                    elif key == "Przewyższenie":
                        try:
                            route_info['elevation_gain_m'] = int(val.replace('m', '').strip())
                        except ValueError:
                            route_info['elevation_gain_m'] = 0
                    elif key == "Czas":
                        try:
                            pattern = re.compile(r'(?:(\d+)\s*h)?\s*(\d+)?\s*min?')
                            match = pattern.search(val)
                            if match:
                                hours = int(match.group(1)) if match.group(1) else 0
                                minutes = int(match.group(2)) if match.group(2) else 0
                                total_minutes = hours * 60 + minutes
                                route_info['time_minutes'] = total_minutes
                            else:
                                route_info['time_minutes'] = 0
                        except Exception as e:
                            print(f"ERROR: Nie udało się sparsować czasu '{val}': {e}")
                            route_info['time_minutes'] = 0
                    elif key == "GPS":
                        route_info['gps_coords'] = val
                    elif key == "Trudność":
                        route_info['difficulty'] = val.lower()
                    elif key == "Opis":
                        route_info['description'] = val
                    elif key in ["Ostrzeżenie", "Ostrzeżenia"]:
                        # Rozbij ostrzeżenia po przecinku lub kropce na listę
                        warnings_list = [w.strip() for w in re.split(r'[,.]', val) if w.strip()]
                        route_info['warnings'].extend(warnings_list)
                    elif key == "Opinie":
                        route_info['reviews'].append(val)

            routes.append(route_info)

        return routes