import csv
import json

def wczytaj_csv(plik):
    with open(plik, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def wczytaj_json(plik):
    with open(plik, encoding='utf-8') as f:
        return json.load(f)