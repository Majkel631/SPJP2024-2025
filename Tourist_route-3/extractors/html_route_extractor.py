import re
from bs4 import BeautifulSoup
from typing import List, Dict

from analyzers.text_processor import TextProcessor


class HTMLWeatherExtractor:
    def parse_html(self, html: str) -> List[Dict]:
        soup = BeautifulSoup(html, 'html.parser')
        weather_data = []

        weather_divs = soup.find_all('div', class_='weather-record')

        for div in weather_divs:
            record = {}

            date_span = div.find('span', class_='date')
            record['date'] = date_span.get_text(strip=True) if date_span else None

            temp_span = div.find('span', class_='temp')
            if temp_span:
                temp_text = temp_span.get_text(strip=True).replace('°C', '')
                try:
                    record['avg_temp'] = float(temp_text)
                except ValueError:
                    record['avg_temp'] = None
            else:
                record['avg_temp'] = None

            desc_span = div.find('span', class_='desc')
            record['description'] = desc_span.get_text(strip=True) if desc_span else None

            location_span = div.find('span', class_='location')
            record['location_id'] = location_span.get_text(strip=True) if location_span else None

            weather_data.append(record)

        return weather_data


class HTMLRouteExtractor:
    def parse_html(self, html: str) -> List[Dict]:
        soup = BeautifulSoup(html, 'html.parser')
        routes = []

        route_divs = soup.find_all('div')

        for div in route_divs:
            h2 = div.find('h2')
            if not h2:
                continue

            route_info = {}
            route_info['name'] = h2.get_text(strip=True)

            route_info['id'] = None
            route_info['length_km'] = 0.0
            route_info['elevation_gain_m'] = 0
            route_info['time_minutes'] = 0
            route_info['gps_coords'] = ''
            route_info['difficulty'] = 'nieznana'
            route_info['description'] = ''
            route_info['reviews'] = []
            route_info['warnings'] = []

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
                        time_minutes = 0
                        match = re.search(r'(?:(\d+)\s*h)?\s*(?:(\d+)\s*min)?', val.lower())
                        if match:
                            hours = int(match.group(1)) if match.group(1) else 0
                            minutes = int(match.group(2)) if match.group(2) else 0
                            time_minutes = hours * 60 + minutes
                        route_info['time_minutes'] = time_minutes
                    elif key in ["Ostrzeżenie", "Ostrzeżenia"]:
                        route_info['warnings'].append(val)
                    elif key == "GPS":
                        route_info['gps_coords'] = val
                    elif key == "Trudność":
                        route_info['difficulty'] = val.lower()
                    elif key == "Opis":
                        route_info['description'] = val
                    elif key == "Opinie":
                        route_info['reviews'].append(val)

            routes.append(route_info)

        return routes