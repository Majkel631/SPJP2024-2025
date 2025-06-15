
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'library.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '..', 'sql', 'schema.sql')

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_database():
    if not os.path.exists(DB_PATH):
        with get_connection() as conn:
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())