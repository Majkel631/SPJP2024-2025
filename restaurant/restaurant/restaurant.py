
from sqlalchemy import func
from db.database import Session
from db.models import Order, OrderItem, Customer, MenuItem, Recipe, Ingredient, RecipeIngredient
from menu.recipe import RecipeManager


class Restaurant:
    def __init__(self):
        self.session = Session()

    def get_by_id(self, restaurant_id):
        return self.session.query(Restaurant).filter_by(id=restaurant_id).first()

    def add_menu_item(self, name, category, price, is_special=False, recipe=None):
        # Sprawdzenie czy kategoria jest poprawna - musi być dokładnie jedną z enumowych wartości
        valid_categories = ["Starter", "Main", "Dessert", "Drink"]
        if category not in valid_categories:
            raise ValueError(f"Kategoria '{category}' nie jest prawidłowa. Wybierz spośród: {valid_categories}")

        menu_item = MenuItem(name=name, category=category, price=price, is_special=is_special)
        self.session.add(menu_item)
        self.session.flush()

        if recipe:
            rec = Recipe(menu_item_id=menu_item.id)
            self.session.add(rec)
            self.session.flush()

            for ingredient_name, qty in recipe.items():
                ingredient_obj = self.session.query(Ingredient).filter_by(name=ingredient_name).first()
                if not ingredient_obj:
                    ingredient_obj = Ingredient(name=ingredient_name, unit_cost=0.0)
                    self.session.add(ingredient_obj)
                    self.session.flush()

                rec_ing = RecipeIngredient(recipe_id=rec.id, ingredient_id=ingredient_obj.id, quantity=qty)
                self.session.add(rec_ing)

        self.session.commit()
        print(f"Dodano danie {name} (kategoria: {category}, cena: {price}) z przepisem.")

    def list_menu(self):
        return self.session.query(MenuItem).all()

    def edit_menu_item(self, name, price=None, is_special=None, recipe=None):
        # Szukamy pozycji o danej nazwie
        item = self.session.query(MenuItem).filter(MenuItem.name == name).first()
        if not item:
            raise ValueError(f"Danie o nazwie '{name}' nie istnieje w menu.")

        # Aktualizujemy jeśli podano nowe wartości
        if price is not None:
            item.price = price
        if is_special is not None:
            item.is_special = is_special

        if recipe is not None:
            recipe_manager = RecipeManager()
            if item.recipe is None:
                # Jeśli brak przepisu - tworzymy nowy
                new_recipe = recipe_manager.create_recipe(item.id, recipe)
                item.recipe = new_recipe
            else:
                # Aktualizujemy istniejący przepis
                recipe_manager.update_recipe(item.recipe.id, recipe)

        self.session.commit()

    def delete_menu_item(self, name):
        # Znajdź danie po nazwie
        item = self.session.query(MenuItem).filter(MenuItem.name == name).first()
        if not item:
            raise ValueError(f"Danie o nazwie '{name}' nie istnieje w menu.")

        # Usuwamy danie
        self.session.delete(item)
        self.session.commit()
        print(f"Usunięto danie '{name}' z menu.")

    def get_most_expensive_dishes(self):
        max_price = self.session.query(func.max(MenuItem.price)).scalar()
        if max_price is None:
            return []
        return self.session.query(MenuItem).filter(MenuItem.price == max_price).all()

    def get_cheapest_dishes(self):
        min_price = self.session.query(func.min(MenuItem.price)).scalar()
        if min_price is None:
            return []
        return self.session.query(MenuItem).filter(MenuItem.price == min_price).all()

    def get_specials_of_day(self):
        return self.session.query(MenuItem).filter(MenuItem.is_special == True).all()

