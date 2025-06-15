from src.database_manager import initialize_database
from src.ui import main_menu

def main():
    initialize_database()
    main_menu()

if __name__ == "__main__":
    main()