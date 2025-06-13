class UserInterface:
    @staticmethod
    def get_preferences():
        return {
            "max_difficulty": input("Maksymalna trudność [1-5]: "),
            "max_length": input("Maksymalna długość trasy [km]: "),
            "preferred_temp": input("Preferowana temperatura [°C]: "),
            "max_precipitation": input("Dopuszczalne opady [mm]: ")
        }

    @staticmethod
    def show_recommendations(recommendations, date):
        print(f"\nRekomendowane trasy na dzień {date}:\n")
        for route, comfort, time_est, categories in recommendations:
            print(f"""
{route.name} ({route.region})
 - Długość: {route.length_km:.1f} km
 - Trudność: {route.difficulty}/5
 - Szacowany czas: {time_est:.2f}h
 - Komfort pogodowy: {comfort}/100
 - Kategoria: {', '.join(categories)}
""")
