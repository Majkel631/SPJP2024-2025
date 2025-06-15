from . import database_manager, repositories

def show_stats():
    stats = repositories.stats()
    print(f"\nLiczba książek: {stats['book_count']}")
    print(f"Liczba autorów: {stats['author_count']}")
    print(f"Najstarsza książka: {stats['oldest']}")
    print(f"Najnowsza książka: {stats['newest']}")
    print(f"Autor z największą liczbą książek: {stats['top_author']}\n")

def manage_authors():
    while True:
        print("\n-- Zarządzanie Autorami --")
        print("1. Dodaj autora")
        print("2. Wyświetl wszystkich autorów")
        print("3. Szukaj autora po nazwisku")
        print("4. Edytuj autora")
        print("5. Usuń autora")
        print("0. Powrót")
        choice = input("Wybierz: ")

        if choice == "1":
            imie = input("Imię: ")
            nazwisko = input("Nazwisko: ")
            rok = input("Rok urodzenia: ")
            narodowosc = input("Narodowość: ")
            repositories.add_author(imie, nazwisko, rok, narodowosc)
            print("Autor dodany pomyślnie.")

        elif choice == "2":
            authors = repositories.get_all_authors()
            if not authors:
                print("Brak autorów w bazie.")
            else:
                print("\nLista autorów:")
                for a in authors:
                    print(f"{a.id}: {a.first_name} {a.last_name}, {a.birth_year}, {a.nationality}")

        elif choice == "3":
            nazwisko = input("Nazwisko: ")
            authors = repositories.find_author_by_last_name(nazwisko)
            if not authors:
                print("Nie znaleziono autora.")
            else:
                for a in authors:
                    print(f"{a.id}: {a.first_name} {a.last_name}, {a.birth_year}, {a.nationality}")

        elif choice == "4":
            try:
                id = int(input("ID autora: "))
            except ValueError:
                print("Nieprawidłowe ID.")
                continue
            imie = input("Imię: ")
            nazwisko = input("Nazwisko: ")
            rok = input("Rok urodzenia: ")
            narodowosc = input("Narodowość: ")
            repositories.update_author(id, imie, nazwisko, rok, narodowosc)
            print("Autor zaktualizowany.")

        elif choice == "5":
            try:
                id = int(input("ID autora: "))
            except ValueError:
                print("Nieprawidłowe ID.")
                continue
            repositories.delete_author(id)
            print("Autor usunięty")

        elif choice == "0":
            break

def manage_books():
    while True:
        print("\n-- Zarządzanie Książkami --")
        print("1. Dodaj książkę")
        print("2. Wyświetl wszystkie książki")
        print("3. Wyszukaj książkę")
        print("4. Edytuj książkę")
        print("5. Usuń książkę")
        print("6. Pokaż książki autora")
        print("0. Powrót")
        choice = input("Wybierz: ")

        if choice == "1":
            tytul = input("Tytuł: ")
            try:
                autor_id = int(input("ID autora: "))
            except ValueError:
                print("Nieprawidłowe ID.")
                continue
            rok = input("Rok wydania: ")
            gatunek = input("Gatunek: ")
            strony = input("Liczba stron: ")
            opis = input("Opis: ")
            repositories.add_book(tytul, autor_id, rok, gatunek, strony, opis)
            print("Książka dodana pomyślnie.")

        elif choice == "2":
            books = repositories.get_all_books()
            if not books:
                print("Brak książek w bazie.")
            else:
                print("\nLista książek:")
                for b in books:
                    print(f"{b.id}: {b.title} ({b.publication_year}) - {b.genre}, {b.pages} str.")

        elif choice == "3":
            fraza = input("Wprowadź tytuł, nazwisko lub rok: ")
            books = repositories.find_books_by_title_or_author_or_year(fraza)
            if not books:
                print("Nie znaleziono książek.")
            else:
                for b in books:
                    print(f"{b.id}: {b.title} ({b.publication_year})")

        elif choice == "4":
            try:
                id = int(input("ID książki: "))
                autor_id = int(input("ID autora: "))
            except ValueError:
                print("Nieprawidłowe dane.")
                continue
            tytul = input("Tytuł: ")
            rok = input("Rok: ")
            gatunek = input("Gatunek: ")
            strony = input("Strony: ")
            opis = input("Opis: ")
            repositories.update_book(id, tytul, autor_id, rok, gatunek, strony, opis)
            print("Książka zaktualizowana.")

        elif choice == "5":
            try:
                id = int(input("ID książki: "))
            except ValueError:
                print("Nieprawidłowe ID.")
                continue
            repositories.delete_book(id)
            print("Książka usunięta.")

        elif choice == "6":
            try:
                id = int(input("ID autora: "))
            except ValueError:
                print("Nieprawidłowe ID.")
                continue
            books = repositories.get_books_by_author(id)
            if not books:
                print("Nie znaleziono książek dla tego autora.")
            else:
                author = next((a for a in repositories.get_all_authors() if a.id == id), None)
                if author:
                    print(f"\nAutor: {author.first_name} {author.last_name}, {author.birth_year}, {author.nationality}")
                print("Książki autora:")
                for b in books:
                    print(f"{b.id}: {b.title} ({b.publication_year}) - {b.genre}, {b.pages} str.")

        elif choice == "0":
            break

def main_menu():
    database_manager.initialize_database()
    while True:
        print("\n=== Biblioteka Domowa ===")
        print("1. Zarządzanie autorami")
        print("2. Zarządzanie książkami")
        print("3. Raporty i statystyki")
        print("0. Wyjście")
        choice = input("Wybierz opcję: ")
        if choice == "1":
            manage_authors()
        elif choice == "2":
            manage_books()
        elif choice == "3":
            show_stats()
        elif choice == "0":
            print("Do zobaczenia!")
            break