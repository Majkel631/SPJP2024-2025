import json
import os

class Config:
    def __init__(self, path=None):
        if path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_dir, 'config.json')
        with open(path, encoding='utf-8') as f:
            config = json.load(f)
            self.db_path = config.get("db_path", "restaurant.db")
            self.starting_balance = config.get("starting_balance", 10000)