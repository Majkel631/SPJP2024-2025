from datetime import datetime
from database.DatabaseReports import DatabaseReports
from database.backup_manager import BackupManager
from database.database_admin import DatabaseAdmin
from database.database_manager import  DatabaseManager
from database.migration_tool import MigrationTool
from database.repositories.route_repository import RouteRepository

def main_menu():
    print("\n=== REKOMENDATOR TRAS TURYSTYCZNYCH ===")
    print("1. Znajdź rekomendowane trasy")
    print("2. Dodaj nową trasę")
    print("3. Statystyki bazy danych")
    print("4. Utwórz kopię zapasową")
    print("5. Importuj dane z CSV")
    print("6. Admin: Statystyki i zarządzanie bazą")
    print("0. Wyjście")


def admin_menu():
    print("\n=== ADMINISTRACJA BAZY DANYCH ===")
    print("1. Pokaż podstawowe statystyki")
    print("2. Sprawdź integralność danych")
    print("3. Usuń stare dane pogodowe")
    print("4. Utwórz kopię zapasową")
    print("0. Powrót")





def main():
    db_path = "data/database/routes.db"
    db_manager = DatabaseManager(db_path)
    db_manager.initialize_database()



    route_repo = RouteRepository(db_manager)
    migration_tool = MigrationTool(db_manager)
    backup_mgr = BackupManager(db_path)
    reports = DatabaseReports(db_path)
    admin = DatabaseAdmin(db_path)

    while True:
        main_menu()
        choice = input("Wybierz opcję: ").strip()

        if choice == "1":
            region = input("Podaj region: ")
            try:
                difficulty = int(input("Maksymalna trudność [1-5]: "))
                results = route_repo.find_by_region_and_difficulty(region, difficulty)
                if results:
                    for r in results:
                        print(f"- {r['name']} | Trudność: {r['difficulty']} | Długość: {r['length_km']} km")
                else:
                    print("Brak wyników.")
            except ValueError:
                print("Nieprawidłowy poziom trudności.")
        elif choice == "2":
            try:
                route_data = {
                    "name": input("Nazwa trasy: "),
                    "region": input("Region: "),
                    "start_lat": float(input("Start lat: ")),
                    "start_lon": float(input("Start lon: ")),
                    "end_lat": float(input("End lat: ")),
                    "end_lon": float(input("End lon: ")),
                    "length_km": float(input("Długość (km): ")),
                    "elevation_gain": int(input("Przewyższenie (m): ")),
                    "difficulty": int(input("Trudność (1-5): ")),
                    "terrain_type": input("Typ terenu: "),
                    "tags": input("Tagi: "),
                    "description": input("Opis: ")
                }
                route_repo.add_route(route_data)
                print("Trasa została dodana.")

                add_weather = input("Czy chcesz dodać dane pogodowe dla tej trasy? (t/n): ").strip().lower()
                if add_weather == 't':
                    avg_temp = float(input("Średnia temperatura (°C): "))
                    min_temp = float(input("Minimalna temperatura (°C): "))
                    max_temp = float(input("Maksymalna temperatura (°C): "))
                    precipitation = float(input("Opady (mm): "))
                    sunshine_hours = float(input("Godziny słoneczne: "))
                    cloud_cover = float(input("Zachmurzenie (0-10): "))

                    weather_data = {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "location_lat": route_data["start_lat"],
                        "location_lon": route_data["start_lon"],
                        "avg_temp": avg_temp,
                        "min_temp": min_temp,
                        "max_temp": max_temp,
                        "precipitation": precipitation,
                        "sunshine_hours": sunshine_hours,
                        "cloud_cover": cloud_cover
                    }
                    db_manager.add_weather_record(weather_data)

                    print("Dane pogodowe zostały dodane.")

            except ValueError:
                print("Błąd danych — upewnij się, że liczby są poprawnie wpisane.")
        elif choice == "3":
            print("\nStatystyki bazy danych:")
            print("- Najpopularniejsze regiony:", reports.most_popular_regions())
            print("- Podsumowanie trudności:", reports.difficulty_summary())
            print("- Statystyki pogodowe:", reports.weather_statistics())
            print("- Trasy bez danych pogodowych:", reports.routes_without_weather())
        elif choice == "4":
            backup_dir = "data/backups"
            backup_path = backup_mgr.create_backup(db_path, backup_dir)
            print(f"Kopia zapasowa została zapisana w: {backup_path}")
        elif choice == "5":
            migration_tool.migrate_routes_from_csv("data/legacy/routes.csv")
            migration_tool.migrate_weather_from_csv("data/legacy/weather.csv")
            print("Dane zostały zaimportowane.")
        elif choice == "6":
            while True:
                admin_menu()
                admin_choice = input("Wybierz opcję administracyjną: ").strip()
                if admin_choice == "1":
                    stats = admin.get_statistics()
                    print(f"Liczba tras: {stats['routes_count']}")
                    print(f"Liczba rekordów pogodowych: {stats['weather_records_count']}")
                elif admin_choice == "2":
                    integrity = admin.check_data_integrity()
                    print(f"Trasy bez danych pogodowych: {integrity['routes_without_weather']}")
                elif admin_choice == "3":
                    days = input("Usuń dane starsze niż ile dni? (domyślnie 365): ").strip()
                    try:
                        days_int = int(days) if days else 365
                        deleted = admin.clean_old_weather_data(days=days_int)
                        print(f"Usunięto {deleted['old_weather']} starych rekordów pogodowych, "
                              f"{deleted['invalid_weather']} bez daty oraz "
                              f"{deleted['routes']} tras.")
                    except ValueError:
                        print("Nieprawidłowa liczba dni.")
                elif admin_choice == "4":
                    backup_dir = "data/backups"
                    backup_path = admin.create_backup(backup_dir)
                    print(f"Kopia zapasowa została utworzona: {backup_path}")
                elif admin_choice == "0":
                    break
                else:
                    print("Nieprawidłowy wybór. Spróbuj ponownie.")
        elif choice == "0":
            db_manager.close()
            reports.close()
            admin.close()
            print("Do zobaczenia!")
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")


if __name__ == "__main__":
    main()