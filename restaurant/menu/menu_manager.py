from db.database import Session
from db.models import MenuItem, Ingredient, menuitem_ingredients
from sqlalchemy.orm import Session as OrmSession

class MenuManager:
    def __init__(self):
        self.session: OrmSession = Session()

    def create_menu_item(self, name: str, category: str, price: float, ingredients_with_qty: dict, is_special=False):
        existing = self.session.query(MenuItem).filter_by(name=name).first()
        if existing:
            raise ValueError(f"Menu item '{name}' already exists.")

        ingredients = []
        for ingr_name, qty in ingredients_with_qty.items():
            ingr = self.session.query(Ingredient).filter_by(name=ingr_name).first()
            if not ingr:
                raise ValueError(f"Ingredient '{ingr_name}' not found in inventory.")
            ingredients.append((ingr, qty))

        menu_item = MenuItem(name=name, category=category, price=price, is_special=is_special)
        self.session.add(menu_item)
        self.session.flush()
        for ingr, qty in ingredients:
            stmt = menuitem_ingredients.insert().values(
                menu_item_id=menu_item.id,
                ingredient_id=ingr.id,
                quantity=qty
            )
            self.session.execute(stmt)

        self.session.commit()
        print(f"Dodano danie '{name}' do menu.")

    def update_menu_item_price(self, name: str, new_price: float):
        item = self.session.query(MenuItem).filter_by(name=name).first()
        if not item:
            raise ValueError(f"Menu item '{name}' not found.")
        item.price = new_price
        self.session.commit()
        print(f"Zaktualizowano cenę dania '{name}' do {new_price}.")

    def set_special(self, name: str, is_special=True):
        item = self.session.query(MenuItem).filter_by(name=name).first()
        if not item:
            raise ValueError(f"Menu item '{name}' not found.")
        item.is_special = is_special
        self.session.commit()
        print(f"Danie '{name}' {'oznaczone jako specjalność' if is_special else 'usunięte ze specjalności'}.")

    def delete_menu_item(self, name: str):
        item = self.session.query(MenuItem).filter_by(name=name).first()
        if not item:
            raise ValueError(f"Menu item '{name}' not found.")
        self.session.delete(item)
        self.session.commit()
        print(f"Danie '{name}' usunięte z menu.")

    def list_menu(self):
        items = self.session.query(MenuItem).order_by(MenuItem.category, MenuItem.name).all()
        for i, item in enumerate(items, 1):
            special = " (Specjalność dnia)" if item.is_special else ""
            print(f"{i}. {item.name} - {item.category} - {item.price} PLN{special}")

    def add_ingredient(self, name: str, unit: str, cost_per_unit: float):
        existing = self.session.query(Ingredient).filter_by(name=name).first()
        if existing:
            raise ValueError(f"Ingredient '{name}' already exists.")
        ingr = Ingredient(name=name, unit=unit, cost_per_unit=cost_per_unit)
        self.session.add(ingr)
        self.session.commit()
        print(f"Dodano składnik '{name}'.")

    def list_ingredients(self):
        ingr_list = self.session.query(Ingredient).all()
        for i, ingr in enumerate(ingr_list, 1):
            print(f"{i}. {ingr.name} - koszt za {ingr.unit}: {ingr.cost_per_unit} PLN")