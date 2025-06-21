
from datetime import datetime, date, timedelta
from sqlalchemy import func
from db.models import Customer as CustomerModel, MenuItem,Ingredient, FinancialTransactionType,  Promotion
from colorama import init, Fore, Style

from restaurant.restaurant import Restaurant
from customers.customer import Customer
from restaurant.restaurant_manager import RestaurantManager
from staff.staff_manager import StaffManager
from inventory.inventory import InventoryManager
from finance.finance import FinanceManager
from db.database import init_db, Base, engine
from menu.marketing import MarketingAndReputationService
def input_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(Fore.RED + "Proszę wpisać poprawną liczbę.")

def input_choice(prompt, choices):
    choices_str = "/".join(choices)
    while True:
        choice = input(f"{prompt} ({choices_str}): ").strip().lower()
        if choice in choices:
            return choice
        print(Fore.RED + f"Proszę wybrać spośród: {choices_str}")


def main():
    Base.metadata.create_all(engine)
    init(autoreset=True)
    restaurant = Restaurant()
    customer = Customer()
    staff_manager = StaffManager()
    inventory_manager = InventoryManager()
    finance_manager = FinanceManager()
    restaurant_manager = RestaurantManager()
    marketing_service = MarketingAndReputationService()
    marketing_service.restaurant = restaurant
    while True:
        print(Style.BRIGHT + "\n--- Symulator Restauracji ---")
        print(Fore.BLUE +"1. Inicjalizuj bazę danych")
        print(Fore.BLUE +"2. Zarządzaj menu")
        print(Fore.BLUE +"3. Zarządzaj klientami")
        print(Fore.BLUE +"4. Wyświetl menu")
        print(Fore.BLUE +"5. Wyświetl klientów")
        print(Fore.BLUE +"6. Zarządzaj pracownikami")
        print(Fore.BLUE +"7. Raporty i statystyki")
        print(Fore.BLUE +"8. Zarządzaj zapasami")
        print(Fore.BLUE +"9. System finansowy")
        print(Fore.BLUE +"10. Rozwój Restauracji")
        print(Fore.BLUE +"11. Marketing i reputacja")
        print(Fore.RED +"0. Wyjście")

        choice = input("Wybierz opcję: ").strip()

        if choice == "1":
            try:
                init_db()
                print(Fore.GREEN + " Baza danych została zainicjowana.")
            except Exception as e:
                print(Fore.RED + f"Błąd inicjalizacji bazy: {e}")

        elif choice == "2":
            while True:
                print(Fore.BLUE +"\n-- Zarządzanie menu --")
                print(Fore.BLUE +"a. Dodaj pozycję")
                print(Fore.BLUE +"b. Edytuj pozycję")
                print(Fore.BLUE +"c. Usuń pozycję")
                print(Fore.BLUE +"d. Wyświetl wszystkie potrawy")
                print(Fore.RED +"e. Wróć")

                subchoice = input("Wybierz opcję: ").strip().lower()

                if subchoice == "a":
                    try:
                        name = input("Nazwa potrawy: ").strip()
                        category_map = {
                            'przystawki': 'Starter',
                            'dania_glowne': 'Main',
                            'desery': 'Dessert',
                            'napoje': 'Drink'
                        }
                        category_input = input_choice("Kategoria", list(category_map.keys()))
                        category = category_map[category_input]
                        price = input_float("Cena PLN: ")
                        is_special = input_choice("Specjalność dnia?", ['tak', 'nie']) == 'tak'

                        recipe = {}
                        if category != 'Drink':
                            num_ingredients = int(input(Fore.GREEN +"Ile składników chcesz dodać? "))
                            for _ in range(num_ingredients):
                                ingredient = input(Fore.BLUE +"Składnik: ").strip()
                                while True:
                                    try:
                                        qty = float(input(Fore.BLUE +f"Ilość dla składnika (Gram) '{ingredient}': "))
                                        break
                                    except ValueError:
                                        print(Fore.RED + "Proszę wpisać poprawną liczbę.")
                                recipe[ingredient] = qty
                        else:
                            print(Fore.RED +"Napoje nie mają składników, pomijam wpisywanie przepisu.")

                        existing = restaurant.session.query(MenuItem).filter(MenuItem.name == name).first()
                        if existing:
                            print(Fore.RED + f"Danie o nazwie '{name}' już istnieje w menu.")
                            continue
                        else:
                            restaurant.add_menu_item(name, category, price, is_special, recipe)
                            print(Fore.GREEN + f" Dodano pozycję: {name}")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")
                    continue

                elif subchoice == "b":
                    try:
                        name = input(Fore.BLUE +"Nazwa potrawy do edycji: ").strip()
                        print(Fore.BLUE +"Zostaw pole puste, jeśli nie chcesz zmieniać wartości.")
                        price_str = input(Fore.BLUE +"Nowa cena (PLN): ").strip()
                        price = float(price_str) if price_str else None
                        special_str = input(Fore.BLUE +"Specjalność dnia (tak/nie): ").strip().lower()
                        is_special = None
                        if special_str == 'tak':
                            is_special = True
                        elif special_str == 'nie':
                            is_special = False

                        change_recipe = input_choice("Czy zmienić przepis?", ['tak', 'nie'])
                        recipe = None
                        if change_recipe == 'tak':
                            recipe = {}
                            num_ingredients = int(input(Fore.BLUE +"Ile składników chcesz dodać? "))
                            for _ in range(num_ingredients):
                                while True:
                                    ingredient = input(Fore.BLUE +"Składnik: ").strip()
                                    if not ingredient:
                                        print(Fore.RED +"Nazwa składnika nie może być pusta, spróbuj ponownie.")
                                        continue
                                    if ingredient in recipe:
                                        print(Fore.RED +"Ten składnik został już dodany, podaj inny.")
                                        continue
                                    break
                                qty = input_float(f"Ilość (Gram) {ingredient}: ")
                                recipe[ingredient] = qty

                        restaurant.edit_menu_item(name, price=price, is_special=is_special, recipe=recipe)
                        print(Fore.GREEN + f"Edytowano pozycję: {name}")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")
                    continue

                elif subchoice == "c":
                    try:
                        name = input(Fore.GREEN +"Nazwa potrawy do usunięcia: ").strip()
                        restaurant.delete_menu_item(name)
                        print(Fore.GREEN + f" Usunięto pozycję: {name}")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")
                    continue

                elif subchoice == "d":
                    try:
                        menu_items = restaurant.list_menu()
                        if not menu_items:
                            print(Fore.RED +"Brak pozycji w menu.")
                        else:
                            print(Fore.BLUE +"\n-- Lista potraw w menu --")
                            for item in menu_items:
                                special = " (Specjalność dnia)" if item.is_special else ""
                                print(f"- {item.name} | Kategoria: {item.category} | Cena: {item.price} PLN{special}")

                                if item.recipe:
                                    ingredients = []
                                    for ri in item.recipe.ingredient_usages:
                                        ingredients.append(f"{ri.ingredient.name} ({ri.quantity} Gram)")
                                    if ingredients:
                                        print("  Składniki: " + ", ".join(ingredients))
                                else:
                                    print(Fore.RED +"  Brak składników.")
                        input("\nNaciśnij Enter, aby kontynuować...")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")
                    continue

                elif subchoice == "e":
                    break

                else:
                    print(Fore.RED + "Niepoprawna opcja.")

        elif choice == "3":
            customer = Customer()

            while True:
                print(Fore.BLUE +"\n-- Zarządzanie klientami --")
                print(Fore.BLUE +"a. Dodaj klienta")
                print(Fore.BLUE +"b. Symuluj napływ klientów")
                print(Fore.BLUE +"c. Wyświetl klientów")
                print(Fore.BLUE +"d. Oceń zadowolenie klientów")
                print(Fore.BLUE +"e. Usuń klienta")
                print(Fore.BLUE +"f. Symuluj kolejkę i rezerwacje")
                print(Fore.BLUE +"g. Wybierz prosty przedmiot dla klienta")
                print(Fore.BLUE +"h. Wybierz zaawansowany przedmiot dla klienta")
                print(Fore.BLUE +"i. Wygeneruj losowe zdarzenie klienta")
                print(Fore.BLUE +"j. Dodaj rezerwację dla klienta")
                print(Fore.BLUE +"k. Pokaż aktualną kolejkę klientów")
                print(Fore.RED +"l. Wróć")

                subchoice = input("Wybierz opcję: ").strip().lower()

                if subchoice == "a":
                    try:
                        budget = input_float("Budżet klienta: ")
                        pref_cat = input_choice("Preferowana kategoria",
                                                ['przystawki', 'dania_glowne', 'desery', 'napoje'])
                        category_map = {
                            'przystawki': 'Starter',
                            'dania_glowne': 'Main',
                            'desery': 'Dessert',
                            'napoje': 'Drink'
                        }
                        internal_cat = category_map.get(pref_cat)
                        customer.add_customer(budget, internal_cat)
                        print(Fore.GREEN + " Dodano klienta.")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "b":
                    try:
                        count = int(input("Liczba klientów do wygenerowania: "))
                        customer.simulate_customers(count)
                        print(Fore.GREEN + f" Wygenerowano {count} klientów.")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "c":
                    try:
                        customers = customer.list_customers()
                        if not customers:
                            print(Fore.YELLOW + "Brak klientów w bazie.")
                        else:
                            print(Style.BRIGHT + f"{'ID':<4} {'Budżet':<8} {'Preferencja'}")
                            print("-" * 30)
                            for c in customers:
                                print(f"{c['id']:<4} {c['budget']:<8.2f} {c['preferred_category']}")

                            # Podmenu po wyświetleniu klientów
                            while True:
                                print("\nCo chcesz zrobić z klientami?")
                                print("1. Usuń klienta")
                                print("2. Wyświetl szczegóły klienta")
                                print("3. Wróć do zarządzania klientami")
                                sub_choice = input("Wybierz opcję: ").strip()

                                if sub_choice == '1':
                                    cust_id_str = input("Podaj ID klienta do usunięcia: ").strip()
                                    if not cust_id_str.isdigit():
                                        print(Fore.RED + "Nieprawidłowy ID klienta.")
                                        continue
                                    try:
                                        cust_id = int(cust_id_str)
                                        customer.delete_customer(cust_id)
                                        print(Fore.GREEN + f"Klient ID={cust_id} został usunięty.")
                                        break
                                    except Exception as e:
                                        print(Fore.RED + f"Błąd: {e}")

                                elif sub_choice == '2':
                                    cust_id_str = input(Fore.BLUE +"Podaj ID klienta do wyświetlenia szczegółów: ").strip()
                                    if not cust_id_str.isdigit():
                                        print(Fore.RED + "Nieprawidłowy ID klienta.")
                                        continue
                                    cust_id = int(cust_id_str)
                                    cust_obj = customer.session.query(CustomerModel).filter_by(id=cust_id).first()
                                    if cust_obj:
                                        print(Fore.BLUE +f"\nSzczegóły klienta ID={cust_obj.id}:")
                                        print(Fore.BLUE +f"Budżet: {cust_obj.budget}")
                                        print(Fore.BLUE +f"Preferencja: {cust_obj.preference}")

                                    else:
                                        print(Fore.RED + "Nie znaleziono klienta o podanym ID.")

                                elif sub_choice == '3':
                                    break

                                else:
                                    print(Fore.RED + "Nieznana opcja. Spróbuj ponownie.")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "d":
                    try:
                        ratings = customer.evaluate_customer_satisfaction()
                        if not ratings:
                            print(Fore.YELLOW + "Brak klientów do oceny.")
                        else:
                            print(Style.BRIGHT + f"{'ID':<5} {'Zadowolenie (%)':<15}")
                            print("-" * 25)
                            for r in ratings:
                                print(f"{r['id']:<5} {r['satisfaction'] * 20:.1f}")  # Przeliczone na 100% (bo max 5)
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "e":
                    try:
                        cust_id_str = input("ID klienta do usunięcia: ").strip()
                        if not cust_id_str.isdigit():
                            print(Fore.RED + "Nieprawidłowy ID klienta.")
                            continue
                        cust_id = int(cust_id_str)
                        customer.delete_customer(cust_id)
                        print(Fore.GREEN + f" Usunięto klienta o ID {cust_id}.")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "f":
                    try:
                        customer.simulate_queue_and_reservations()
                        print(Fore.GREEN + " Symulacja kolejki i rezerwacji zakończona.")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "g":
                    try:
                        cust_id_str = input(Fore.BLUE +"ID klienta: ").strip()
                        if not cust_id_str.isdigit():
                            raise ValueError(Fore.BLUE +"Nieprawidłowy ID klienta.")
                        cust_id = int(cust_id_str)
                        cust_obj = customer.session.query(CustomerModel).filter_by(id=cust_id).first()
                        if not cust_obj:
                            raise ValueError(Fore.BLUE +"Nie znaleziono klienta o podanym ID.")
                        menu_items = customer.session.query(MenuItem).all()
                        item = customer.choose_item(menu_items)
                        if item:
                            print(
                                Fore.BLUE +  f"Wybrano prosty przedmiot dla klienta {cust_id}: {item.name} ({item.category}) - {item.price}")
                        else:
                            print(Fore.RED +"Brak dostępnych przedmiotów.")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "h":
                    try:
                        cust_id_str = input(Fore.BLUE +"ID klienta: ").strip()
                        if not cust_id_str.isdigit():
                            raise ValueError(Fore.RED +"Nieprawidłowy ID klienta.")
                        cust_id = int(cust_id_str)
                        cust_obj = customer.session.query(CustomerModel).filter_by(id=cust_id).first()
                        if not cust_obj:
                            raise ValueError(Fore.RED +"Nie znaleziono klienta o podanym ID.")
                        menu_items = customer.session.query(MenuItem).all()
                        item = customer.choose_item_advanced(cust_obj, menu_items)
                        if item:
                            print(
                                Fore.GREEN + f"Wybrano zaawansowany przedmiot dla klienta {cust_id}: {item.name} ({item.category}) - {item.price}")
                        else:
                            print(Fore.RED +"Brak dostępnych przedmiotów pasujących do preferencji i budżetu.")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "i":
                    try:
                        cust_id_str = input("ID klienta: ").strip()
                        if not cust_id_str.isdigit():
                            raise ValueError(Fore.RED +"Nieprawidłowy ID klienta.")
                        cust_id = int(cust_id_str)
                        customer.random_customer_event(cust_id)
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "j":
                    try:
                        cust_id_str = input("ID klienta: ").strip()
                        if not cust_id_str.isdigit():
                            raise ValueError("Nieprawidłowy ID klienta.")
                        cust_id = int(cust_id_str)

                        datetime_str = input("Data i godzina rezerwacji (YYYY-MM-DD HH:MM): ").strip()
                        try:
                            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                        except ValueError:
                            print(
                                Fore.RED + "Nieprawidłowy format daty lub nieistniejąca data. Użyj formatu YYYY-MM-DD HH:MM, np. 2025-06-20 19:30.")
                            continue  # wraca do menu zarządzania klientami

                        table_number_str = input(Fore.BLUE +"Numer stolika: ").strip()
                        if not table_number_str.isdigit():
                            raise ValueError(Fore.RED +"Nieprawidłowy numer stolika.")
                        table_number = int(table_number_str)

                        customer.make_reservation(cust_id, datetime_obj, table_number)
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "k":
                    try:
                        queue = customer.get_queue()
                        if not queue:
                            print(Fore.YELLOW + "Brak klientów w kolejce.")
                        else:
                            print(Fore.GREEN +"Aktualna kolejka klientów:")
                            for w in queue:
                                print(f"Klient ID={w.customer_id}, czas przyjścia: {w.arrival_time}")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "l":
                    break

                else:
                    print(Fore.RED + "Niepoprawna opcja.")
        elif choice == "4":
            try:
                menu_items = restaurant.list_menu()
                if not menu_items:
                    print(Fore.RED +"Brak pozycji w menu.")
                else:
                    print(Fore.BLUE +"\n-- Menu restauracji --")
                    for item in menu_items:
                        special = " (Specjalność dnia)" if item.is_special else ""
                        print(Fore.BLUE +f"- {item.name} | Kategoria: {item.category} | Cena: {item.price} PLN{special}")
                input("\nNaciśnij Enter, aby kontynuować...")
            except Exception as e:
                print(Fore.RED + f"Błąd: {e}")

        elif choice == "5":
            try:
                customers_list = customer.list_customers()
                if not customers_list:
                    print(Fore.RED +"Brak klientów.")
                else:
                    print("\n-- Lista klientów --")
                    for cust in customers_list:
                        print(Fore.GREEN +f"ID: {cust['id']} | Budżet: {cust['budget']} PLN | Preferowana kategoria: {cust['preferred_category']}")
                input("\nNaciśnij Enter, aby kontynuować...")
            except Exception as e:
                print(Fore.RED + f"Błąd: {e}")

        elif choice == "6":
            while True:
                print(Fore.BLUE +"\n-- Zarządzanie pracownikami --")
                print(Fore.BLUE +"a. Dodaj pracownika")
                print(Fore.BLUE +"b. Usuń pracownika")
                print(Fore.BLUE +"c. Wyświetl pracowników")
                print(Fore.BLUE +"d. Przydziel zmianę")
                print(Fore.BLUE +"e. Przyznaj premię")
                print(Fore.BLUE +"f. Przeszkol pracownika")
                print(Fore.BLUE +"g. Oceń jakość pracy")
                print(Fore.BLUE +"h. Zaktualizuj wydajność")
                print(Fore.BLUE +"i. Zaktualizuj zadowolenie")
                print(Fore.RED +"j. Powrót")

                subchoice = input("Wybierz opcję: ").strip().lower()

                if subchoice == "a":
                    try:
                        name = input("Imię i nazwisko pracownika: ").strip()
                        role_map = {
                            'kelner': 'Waiter',
                            'kucharz': 'Chef',
                            'manager': 'Manager',
                            'barman': 'Bartender'
                        }
                        print(Fore.BLUE +"Dostępne role: kelner, kucharz, manager, barman")
                        role_input = input("Podaj rolę: ").strip().lower()
                        if role_input not in role_map:
                            raise ValueError(Fore.RED +"Nieprawidłowa rola.")
                        role = role_map[role_input]
                        staff_manager.add_staff(name, role)
                        print(Fore.GREEN + f" Dodano pracownika: {name} jako {role}.")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "b":
                    try:
                        staff_id = int(input("ID pracownika do usunięcia: "))
                        staff_manager.delete_staff(staff_id)
                        print(Fore.GREEN + f"✔ Usunięto pracownika o ID {staff_id}.")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "c":
                    try:
                        staff_list = staff_manager.list_staff()
                        if not staff_list:
                            print("Brak pracowników.")
                        else:
                            print(Style.BRIGHT + f"{'ID':<5} {'Imię i nazwisko':<20} {'Rola'}")
                            print("-" * 40)
                            for s in staff_list:
                                print(f"{s.id:<5} {s.name:<20} {s.role}")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "d":
                    try:
                        staff_id = int(input(Fore.BLUE +"ID pracownika: "))
                        shift = input(Fore.BLUE +"Podaj zmianę (np. 'Poranna', 'Wieczorna'): ").strip()
                        staff_manager.assign_shift(staff_id, shift)
                        print(Fore.GREEN + "Zmiana została przydzielona.")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "e":
                    try:
                        staff_id = int(input(Fore.BLUE +"ID pracownika: "))
                        amount = float(input(Fore.BLUE +"Kwota premii: "))
                        staff_manager.grant_bonus(staff_id, amount)
                        print(Fore.GREEN + "Premia została przyznana.")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "f":
                    try:
                        staff_id = int(input("ID pracownika: "))
                        skill_inc = float(input("Wzrost umiejętności (np. 0.5): "))
                        staff_manager.train_staff(staff_id, skill_inc)
                        print(Fore.GREEN + "✔ Pracownik przeszedł szkolenie.")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "g":
                    try:
                        staff_id = int(input("ID pracownika: "))
                        quality = staff_manager.evaluate_quality(staff_id)
                        print(Fore.GREEN +f"Jakość pracy pracownika ID={staff_id} wynosi: {quality:.2f}")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "h":
                    try:
                        staff_id = int(input("ID pracownika: "))
                        perf_score = float(input("Nowy wynik wydajności: "))
                        staff_manager.update_performance(staff_id, perf_score)
                        print(Fore.GREEN + " Wydajność została zaktualizowana.")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "i":
                    try:
                        staff_id = int(input(Fore.BLUE +"ID pracownika: "))
                        satisfaction = float(input("Poziom zadowolenia (np. 0.0 - 1.0): "))
                        staff_manager.update_satisfaction(staff_id, satisfaction)
                        print(Fore.GREEN + " Zadowolenie zostało zaktualizowane.")
                    except Exception as e:
                        print(Fore.RED + f"Błąd: {e}")

                elif subchoice == "j":
                    break

                else:
                    print(Fore.RED + "Niepoprawna opcja.")

        elif choice == "7":
            while True:
                print(Fore.BLUE +"\n-- Raporty i statystyki --")
                print(Fore.BLUE +"a. Najdroższe potrawy")
                print(Fore.BLUE +"b. Najtańsze potrawy")
                print(Fore.BLUE +"c. Specjalności dnia")
                print(Fore.RED +"d. Wróć")

                subchoice = input(Fore.BLUE +"Wybierz opcję: ").strip().lower()

                if subchoice == "a":
                    expensive = restaurant.get_most_expensive_dishes()
                    if expensive:
                        print(Fore.GREEN +"Najdroższe potrawy:")
                        for dish in expensive:
                            print(f"- {dish.name} | Cena: {dish.price} PLN")
                    else:
                        print(Fore.RED +"Brak danych.")
                    input("\nNaciśnij Enter, aby kontynuować...")

                elif subchoice == "b":
                    cheap = restaurant.get_cheapest_dishes()
                    if cheap:
                        print(Fore.GREEN +"Najtańsze potrawy:")
                        for dish in cheap:
                            print(f"- {dish.name} | Cena: {dish.price} PLN")
                    else:
                        print(Fore.RED +"Brak danych.")
                    input("\nNaciśnij Enter, aby kontynuować...")

                elif subchoice == "c":
                    specials = restaurant.get_specials_of_day()
                    if specials:
                        print(Fore.BLUE +"Specjalności dnia:")
                        for dish in specials:
                            print(f"- {dish.name} | Cena: {dish.price} PLN")
                    else:
                        print(Fore.RED +"Brak specjalności dnia.")
                    input("\nNaciśnij Enter, aby kontynuować...")

                elif subchoice == "d":
                    break

                else:

                  print(Fore.RED + "Niepoprawna opcja.")

        elif choice == "8":
            while True:
                print(Fore.BLUE +"\n-- Zarządzanie zapasami --")
                print(Fore.BLUE +"a. Przeglądaj zapasy składników")
                print(Fore.BLUE +"b. Zużyj składniki przy przygotowaniu potrawy (pojedynczy składnik)")
                print(Fore.BLUE +"c. Zamów nowe surowce")
                print(Fore.BLUE +"d. Sugestie zamówień")
                print(Fore.BLUE +"e. Monitoruj przeterminowane składniki")
                print(Fore.BLUE +"f. Zarządzaj składnikami specjalnymi i sezonowymi")
                print(Fore.RED +"g. Wróć")

                subchoice = input("Wybierz opcję: ").strip().lower()

                if subchoice == "a":
                    inventory_items = inventory_manager.list_inventory()
                    if inventory_items:
                        print(Fore.BLUE +"Aktualne zapasy składników:")
                        for item in inventory_items:
                            expiry_str = item.expiry_date.date() if item.expiry_date else "brak daty ważności"
                            print(f"- {item.ingredient.name}: {item.quantity} (ważne do {expiry_str})")
                    else:
                        print(Fore.RED +"Brak zapasów.")
                    input("\nNaciśnij Enter, aby kontynuować...")

                elif subchoice == "b":
                    ingredient_name = input(Fore.BLUE +"Nazwa składnika do zużycia: ").strip()
                    amount = float(input(Fore.BLUE +"Ilość do zużycia: "))
                    ingredient = (inventory_manager.session.query(Ingredient)
                                  .filter(func.lower(Ingredient.name) == ingredient_name.lower())
                                  .first())
                    if not ingredient:
                        print(Fore.RED +"Nie znaleziono składnika.")
                    else:
                        try:
                            inventory_manager.consume_ingredient(ingredient.id, amount)
                            print(Fore.RED +"Składniki zostały zużyte.")
                        except Exception as e:
                            print(Fore.RED +f"Błąd: {e}")
                    input("\nNaciśnij Enter, aby kontynuować...")

                elif subchoice == "c":
                    supplier_name = input(Fore.BLUE +"Podaj nazwę dostawcy: ").strip()
                    ingredient_name = input(Fore.BLUE +"Nazwa składnika do zamówienia: ").strip()
                    quantity = float(input(Fore.BLUE +"Ilość do zamówienia: "))

                    is_special_input = input(Fore.BLUE +"Czy to składnik specjalny? (tak/nie): ").strip().lower()
                    is_special = (is_special_input == "tak")

                    is_seasonal = False
                    season = ""

                    if is_special:
                        is_seasonal_input = input(Fore.BLUE +"Czy składnik jest sezonowy? (tak/nie): ").strip().lower()
                        is_seasonal = (is_seasonal_input == "tak")
                        if is_seasonal:
                            season = input(Fore.BLUE +"Podaj sezon (np. Lato, Zima): ").strip()

                    try:
                        inventory_manager.order_ingredient(supplier_name, ingredient_name, quantity, is_special,
                                                           is_seasonal, season)
                        print(Fore.GREEN +"Zamówienie zostało złożone.")
                    except ValueError as e:
                        print(Fore.RED +f"Błąd: {e}")
                    input("\nNaciśnij Enter, aby kontynuować...")

                elif subchoice == "d":
                    suggestions = inventory_manager.suggest_orders()
                    if suggestions:
                        print(Fore.BLUE +"Sugestie zamówień:")
                        for name, qty in suggestions:
                            print(Fore.BLUE + f"- {name}: sugerowana ilość {qty}")
                    else:
                        print(Fore.RED +"Brak sugestii.")
                    input("\nNaciśnij Enter, aby kontynuować...")

                elif subchoice == "e":
                    expired = inventory_manager.expired_items()
                    if expired:
                        print(Fore.BLUE +"Przeterminowane składniki:")
                        for item in expired:
                            print(
                                Fore.RED +  f"- {item.ingredient.name}: {item.quantity} (przeterminowany {item.expiry_date.date()})")
                    else:
                        print(Fore.RED +"Brak przeterminowanych składników.")
                    input("\nNaciśnij Enter, aby kontynuować...")

                elif subchoice == "f":
                    season = input(Fore.BLUE +"Podaj sezon (np. Lato, Zima): ").strip()
                    specials = inventory_manager.seasonal_ingredients(season)
                    if specials:
                        print(Fore.BLUE +"Składniki specjalne i sezonowe:")
                        for ingredient in specials:
                            print(f"- {ingredient.name}")
                    else:
                        print(Fore.RED +"Brak składników specjalnych lub sezonowych.")
                    input( "\nNaciśnij Enter, aby kontynuować...")

                elif subchoice == "g":
                    break

                else:
                    print(Fore.RED +"Niepoprawna opcja.")

        elif choice == "9":

            while True:
                print(Fore.BLUE +"\n--- System Finansowy ---")
                print(Fore.BLUE +"1. Wyświetl stan konta")
                print(Fore.BLUE +"2. Dodaj przychód lub wydatek")
                print(Fore.BLUE +"3. Wypłać pensje")
                print(Fore.BLUE +"4. Opłać czynsz")
                print(Fore.BLUE +"5. Zakup sprzętu")
                print(Fore.BLUE +"6. Nalicz podatek")
                print(Fore.BLUE +"7. Raport finansowy")
                print(Fore.BLUE +"8. Prognoza zysków")
                print(Fore.BLUE +"9. Zaciągnij kredyt")
                print(Fore.GREEN +"0. Powrót")

                sub_choice = input("Wybierz opcję: ")

                if sub_choice == "1":
                    balance = finance_manager.get_budget_balance()
                    print(
                        Fore.BLUE + f"Aktualny stan konta: {balance:.2f} zł" if balance is not None else Fore.RED + "Brak danych budżetowych.")

                elif sub_choice == "2":
                    income = float(input(Fore.BLUE +"Podaj kwotę przychodu (0 jeśli brak): "))
                    expense = float(input(Fore.BLUE +"Podaj kwotę wydatku (0 jeśli brak): "))
                    desc_income = ""
                    desc_expense = ""
                    if income != 0:
                        desc_income = input(Fore.BLUE +"Opis transakcji przychodu: ")
                        finance_manager.record_transaction(amount=income, type_=FinancialTransactionType.INCOME,
                                              description=desc_income)
                        print(Fore.GREEN +" Transakcja przychodu dodana.")

                    if expense != 0:
                        desc_expense = input(Fore.BLUE +"Opis transakcji wydatku: ")
                        finance_manager.record_transaction(amount=-expense, type_=FinancialTransactionType.EXPENSE,
                                              description=desc_expense)
                        print(Fore.GREEN +" Transakcja wydatku dodana.")
                elif sub_choice == "3":
                    finance_manager.pay_salaries()
                    print( Fore.GREEN + "Wypłacono pensje.")

                elif sub_choice == "4":
                    amount = float(input(Fore.BLUE +"Kwota czynszu: "))
                    finance_manager.pay_rent(amount)
                    print(Fore.GREEN +" Czynsz opłacony.")

                elif sub_choice == "5":
                    amount = float(input(Fore.BLUE +"Kwota zakupu: "))
                    desc = input(Fore.BLUE +"Opis sprzętu: ")
                    finance_manager.purchase_equipment(amount, description=desc)
                    print(Fore.GREEN +"Sprzęt zakupiony.")

                elif sub_choice == "6":
                    amount = float(input(Fore.BLUE +"Kwota podatku: "))
                    finance_manager.charge_tax(amount)
                    print(Fore.BLUE +" Podatek naliczony.")

                elif sub_choice == "7":
                    period = input(Fore.BLUE +"Okres (daily / weekly / monthly): ").lower()
                    report = finance_manager.get_financial_report(period)
                    print(Fore.BLUE +f"\n Raport za okres '{period}':")
                    print(Fore.BLUE +f"Przychody: {report['income']:.2f} zł")
                    print(Fore.BLUE +f"Wydatki: {report['expenses']:.2f} zł")
                    print(Fore.BLUE +f"Zysk netto: {report['net_profit']:.2f} zł")

                elif sub_choice == "8":
                    forecast = finance_manager.forecast_next_month()
                    print(Fore.BLUE +"\n Prognoza na następny miesiąc:")
                    print(Fore.BLUE +f"Średni dzienny zysk: {forecast['avg_daily_profit']:.2f} zł")
                    print(Fore.BLUE +f"Prognozowany zysk: {forecast['forecast_next_month']:.2f} zł")

                elif sub_choice == "9":
                    amount = float(input(Fore.BLUE +"Kwota kredytu: "))
                    desc = input(Fore.BLUE +"Opis kredytu: ")
                    finance_manager.take_loan(amount, description=desc)
                    print(Fore.GREEN +" Kredyt zaciągnięty.")

                elif sub_choice == "0":
                    break

                else:
                    print(Fore.RED +" Nieprawidłowa opcja.")

        elif choice == "10":
                while True:
                    print(Fore.BLUE +"\n-- Rozwój Restauracji --")
                    print(Fore.BLUE +"a. Dodaj sprzęt")
                    print(Fore.BLUE +"b. Dodaj stolik")
                    print(Fore.BLUE +"c. Zmień atmosferę")
                    print(Fore.BLUE +"d. Zmień układ restauracji")
                    print(Fore.BLUE +"e. Lista sprzętu")
                    print(Fore.BLUE +"f. Lista stolików")
                    print(Fore.BLUE +"g. Lista atmosfer")
                    print(Fore.BLUE +"h. Lista układów")
                    print(Fore.GREEN +"i. Wróć")

                    sub = input("Wybierz opcję: ").strip().lower()

                    if sub == "a":
                        try:
                            name = input(Fore.BLUE +"Nazwa sprzętu: ")
                            eq_type = input(Fore.BLUE +"Typ sprzętu: ")
                            efficiency = input_float(Fore.BLUE +"Efektywność (0.0 - 1.0): ")
                            description = input("Opis: ")
                            restaurant_manager.add_equipment(name, eq_type, efficiency, description)
                            print(Fore.GREEN + " Dodano sprzęt.")
                        except Exception as e:
                            print(Fore.RED + f"Błąd: {e}")

                    elif sub == "b":
                        try:
                            number = int(input(Fore.BLUE +"Numer stolika: "))
                            seats = int(input(Fore.BLUE +"Liczba miejsc: "))
                            location = input(Fore.BLUE +"Lokalizacja: ")
                            description = input(Fore.BLUE +"Opis: ")
                            restaurant_manager.add_table(number, seats, location, description)
                            print(Fore.GREEN + Fore.BLUE +" Dodano stolik.")
                        except Exception as e:
                            print(Fore.RED + f"Błąd: {e}")

                    elif sub == "c":
                        try:
                            style = input(Fore.BLUE +"Styl (np. Klasyczny, Nowoczesny): ")
                            description = input("Opis stylu: ")
                            effect = input_float("Wpływ na satysfakcję klienta (np. 0.1): ")
                            restaurant_manager.set_atmosphere(style, description, effect)
                            print(Fore.GREEN + "Zmieniono atmosferę.")
                        except Exception as e:
                            print(Fore.RED + f"Błąd: {e}")

                    elif sub == "d":
                        try:
                            layout = input( Fore.BLUE +  "Nazwa układu: ")
                            description = input(Fore.BLUE +"Opis układu: ")
                            restaurant_manager.set_layout(layout, description)
                            print(Fore.GREEN + " Układ zaktualizowany.")
                        except Exception as e:
                            print(Fore.RED + f"Błąd: {e}")

                    elif sub == "e":
                        equipment_list = restaurant_manager.get_equipment_list()
                        if equipment_list:
                            print("\n-- Lista sprzętu --")
                            for eq in equipment_list:
                                print(Fore.BLUE +
                                    f"{eq.id}. {eq.name} | Typ: {eq.type} | Efektywność: {eq.efficiency:.2f} | Stan: {eq.condition:.1f}%")
                        else:
                            print(Fore.RED  + "Brak sprzętu.")

                    elif sub == "f":
                        tables = restaurant_manager.get_tables()
                        if tables:
                            print(Fore.BLUE  + "\n-- Lista stolików --")
                            for t in tables:
                                print(
                                    f"{t.id}. Nr {t.number} | Miejsca: {t.seats} | Rezerwacja: {'Tak' if t.is_reserved else 'Nie'}")
                        else:
                            print(Fore.RED  + "Brak stolików.")

                    elif sub == "g":
                        atmospheres = restaurant_manager.get_atmospheres()
                        if atmospheres:
                            print(Fore.BLUE +  "\n-- Style atmosfery --")
                            for a in atmospheres:
                                print(
                                    f"{a.name} | Opis: {a.description} | Wpływ: {a.customer_satisfaction_modifier}")
                        else:
                            print(Fore.RED  + "Brak atmosfer.")

                    elif sub == "h":
                        layouts = restaurant_manager.get_layouts()
                        if layouts:
                            print("\n-- Układy restauracji --")
                            for l in layouts:
                                print( Fore.BLUE  + f"{l.layout_name} | Opis: {l.description}")
                        else:
                            print( Fore.RED  + "Brak układów.")

                    elif sub == "i":
                        break

                    else:
                        print(Fore.RED + "Niepoprawna opcja.")

        elif choice == "11":
            while True:
                print(Fore.BLUE +"\n-- Marketing i Reputacja --")
                print(Fore.BLUE +"a. Dodaj opinię klienta")
                print(Fore.BLUE +"b. Uruchom kampanię marketingową")
                print(Fore.BLUE +"c. Zastosuj promocję dla klienta")
                print(Fore.BLUE +"d. Dodaj punkty lojalnościowe za zakup")
                print(Fore.BLUE +"e. Wymień punkty lojalnościowe")
                print(Fore.BLUE +"f. Zaktualizuj reputację po recenzji medialnej")
                print(Fore.GREEN +"g. Wróć")

                subchoice = input(Fore.GREEN + "Wybierz opcję: ").strip().lower()

                try:
                    if subchoice == "a":
                        customer_id = int(input(Fore.GREEN + "ID klienta: "))
                        rating = int(input(Fore.GREEN + "Ocena (1–5): "))
                        comment = input(Fore.GREEN + "Komentarz: ").strip()

                        customer = marketing_service.session.get(CustomerModel, customer_id)
                        if not customer:
                            print(Fore.RED +"Nie znaleziono klienta.")
                            continue

                        # Tu wywołanie bez restauracji — tak jak masz w klasie
                        marketing_service.submit_review(customer, rating, comment)
                        print(Fore.GREEN +"Dodano opinię i zaktualizowano reputację.")

                    elif subchoice == "b":
                        campaign_id = int(input(Fore.GREEN + "ID kampanii marketingowej: "))
                        if marketing_service.run_marketing_campaign(campaign_id):
                            print(Fore.GREEN +"Kampania uruchomiona.")
                        else:
                            print(Fore.RED +"Kampania jest poza datą ważności.")

                    elif subchoice == "c":
                        customer_id = int(input(Fore.BLUE + "ID klienta: "))
                        promotion_id = int(input( Fore.BLUE +"ID promocji: "))

                        customer = marketing_service.session.get(CustomerModel, customer_id)
                        promotion = marketing_service.session.get(Promotion, promotion_id)

                        if not customer:
                            print(Fore.RED + "Nie znaleziono klienta.")
                            continue

                        if not promotion:

                            restaurant = marketing_service.get_or_create_restaurant()
                            promotion = Promotion(
                                restaurant_id=restaurant.id,
                                title="Promocja domyślna",
                                description="Domyślna zniżka",
                                discount_percent=10.0,
                                start_date=date.today(),
                                end_date=date.today() + timedelta(days=7)
                            )
                            marketing_service.session.add(promotion)
                            marketing_service.session.commit()
                            marketing_service.session.refresh(promotion)


                        if marketing_service.apply_promotion(customer, promotion):
                            print(Fore.GREEN + "Promocja zastosowana – dodano punkty lojalnościowe.")
                        else:
                            print(Fore.RED +"Promocja nieaktywna.")
                    elif subchoice == "d":
                        customer_id = int(input(Fore.GREEN + "ID klienta: "))
                        amount = float(input(Fore.GREEN + "Kwota zakupu (PLN): "))
                        customer = marketing_service.session.get(CustomerModel, customer_id)

                        if not customer:
                            print(Fore.RED + "Nie znaleziono klienta.")
                            continue

                        points = marketing_service.add_loyalty_points(customer, amount)
                        print(Fore.GREEN + f"Dodano {points} punktów lojalnościowych.")

                    elif subchoice == "e":
                        customer_id = int(input("ID klienta: "))
                        customer = marketing_service.session.get(CustomerModel, customer_id)

                        if not customer:
                            print(Fore.RED + "Nie znaleziono klienta.")
                            continue

                        if marketing_service.redeem_loyalty_points(customer):
                            print(Fore.GREEN +"Punkty wymienione na nagrodę.")
                        else:
                            print(Fore.RED +"Za mało punktów.")
                    elif subchoice == "f":
                        media_id = int(input("ID recenzji medialnej: "))
                        marketing_service.media_review_effect(media_id)
                        print(Fore.GREEN + "Reputacja zaktualizowana na podstawie recenzji medialnej.")

                    elif subchoice == "g":
                        break

                    else:
                        print(Fore.RED + "Nieznana opcja.")

                except Exception as e:
                    print(Fore.RED + "Błąd: {e}")

        elif choice == "0":
            print(Fore.RED + "Koniec programu. Do widzenia!")
            break
if __name__ == "__main__":
    main()
