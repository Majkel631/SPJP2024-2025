
def parse_reviews(s):
    try:
        return ast.literal_eval(s)
    except Exception:
        return []

import ast

def parse_reviews(s):
    try:
        return ast.literal_eval(s)
    except Exception:
        return []

def preprocess_row(row):
    raw_diff = row.get("difficulty", "").strip().lower()

    difficulty_map = {
        "łatwa": "łatwa",
        "atwa": "łatwa",
        "łatw": "łatwa",
        "rednia": "średnia",
        "średnia": "średnia",
        "trudna": "trudna",
    }

    difficulty = difficulty_map.get(raw_diff, "nieznana")

    route_id = row.get("id")
    if route_id is None:
        raise ValueError("Brak klucza 'id' w wierszu danych")

    warnings_raw = row.get("warnings", "[]")
    try:
        warnings = ast.literal_eval(warnings_raw) if isinstance(warnings_raw, str) else warnings_raw
    except Exception:
        warnings = []

    return {
        "id": route_id,
        "name": row["name"],
        "length_km": float(row.get("length_km", 0)),
        "elevation_gain_m": int(row.get("elevation_gain_m", 0)),
        "time_minutes": int(row.get("time_minutes", 0)),
        "gps_coords": row.get("gps_coords", None),
        "difficulty": difficulty,
        "description": row.get("description", ""),
        "reviews": parse_reviews(row.get("reviews", "[]")),
        "warnings": warnings,
    }