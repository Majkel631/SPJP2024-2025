from moduly.loader import wczytaj_csv
from moduly.filtracja import filtruj_trasy
from moduly.statystyki import srednia_temp, suma_opadow, liczba_dni_slonecznych

def pogoda_dla_regionu(pogoda, region):
    return list(filter(lambda d: d['region'] == region, pogoda))

# Wczytanie danych
trasy = wczytaj_csv('dane/trasy.csv')
pogoda = wczytaj_csv('dane/pogoda.csv')

# --- Interaktywny wybór regionu ---
dostepne_regiony = sorted(set(trasa['region'] for trasa in trasy))

print("Dostępne regiony tras:")
for r in dostepne_regiony:
    print(f" - {r}")

region_docelowy = input("\nWpisz nazwę regionu, który Cię interesuje: ").strip()

if region_docelowy not in dostepne_regiony:
    print(" Podany region nie istnieje w danych.")
else:
    # --- Trasy w regionie ---
    wybrane_trasy = filtruj_trasy(trasy, region=region_docelowy)
    print(f"\n✅ Wybrane trasy w regionie: {region_docelowy}")
    for t in wybrane_trasy:
        print(f"""
        • Nazwa: {t['nazwa']}
        • Długość: {t['dlugosc_km']} km
        • Trudność: {t['trudnosc']}
        • Przewyższenie: {t['przewyzszenie']} m
        • Teren: {t['teren']}
        • Lokalizacja: {t.get('lokalizacja', 'brak danych')}
        """)

    # --- Pogoda dla regionu ---
    pogoda_region = pogoda_dla_regionu(pogoda, region_docelowy)

    print(f"\n📊 Statystyki pogodowe dla regionu: {region_docelowy}")
    print(f"Średnia temperatura: {srednia_temp(pogoda_region):.2f}°C")
    print(f"Suma opadów: {suma_opadow(pogoda_region):.2f} mm")
    print(f"Liczba dni słonecznych: {liczba_dni_slonecznych(pogoda_region)} dni")