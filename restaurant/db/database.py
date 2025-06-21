import os
from sqlite3 import OperationalError

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

DATABASE_URL = "sqlite:///restaurant.db"

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

def init_db():
    try:
        if os.path.exists("restaurant.db"):
            os.remove("restaurant.db")
            print("Usunięto starą bazę danych.")
        Base.metadata.create_all(engine)
        print("Nowa baza danych SQLite zainicjowana.")
    except PermissionError as e:
        print(f"Błąd inicjalizacji bazy: {e}")
    except OperationalError as e:
        print(f"Błąd SQLAlchemy: {e}")