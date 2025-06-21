from db.database import Session
from db.models import InventoryItem, Ingredient, Order, Recipe, Supplier, SupplyOrder, SupplyOrderItem
from datetime import datetime, timedelta
from sqlalchemy import func


class InventoryManager:
    def __init__(self):
        self.session = Session()

    # 1. Śledzenie ilości i dat ważności składników
    def list_inventory(self):
        """Zwraca listę wszystkich składników wraz z ilością i datą ważności."""
        return self.session.query(InventoryItem).join(Ingredient).all()

    # 2. Zużywanie składników przy przygotowaniu potraw
    def consume_ingredient(self, ingredient_id: int, amount: float):
        """Zużywa określoną ilość składnika z magazynu, zaczynając od najstarszych zapasów."""
        items = (self.session.query(InventoryItem)
                 .filter(InventoryItem.ingredient_id == ingredient_id, InventoryItem.quantity > 0)
                 .order_by(InventoryItem.expiry_date)
                 .all())

        remaining = amount
        for item in items:
            if item.quantity >= remaining:
                item.quantity -= remaining
                remaining = 0
                break
            else:
                remaining -= item.quantity
                item.quantity = 0

        if remaining > 0:
            raise ValueError("Niewystarczająca ilość składnika w magazynie.")
        self.session.commit()

    # 2b. Automatyczne zużywanie składników dla potrawy
    def consume_ingredients_for_dish(self, dish_name: str):
        """Na podstawie nazwy potrawy zużywa wszystkie potrzebne składniki."""
        recipe = self.session.query(Recipe).filter(func.lower(Recipe.name) == dish_name.lower()).first()
        if not recipe:
            raise ValueError("Nie znaleziono przepisu na tę potrawę.")

        for rec_ing in recipe.ingredient_usages:
            self.consume_ingredient(rec_ing.ingredient_id, rec_ing.quantity)

    # 3. Zamawianie nowych surowców
    def order_ingredient(self, supplier_name: str, ingredient_name: str, quantity: float,
                         is_special: bool = False, is_seasonal: bool = False, season: str = ""):
        # Znajdź lub utwórz dostawcę
        supplier = self.session.query(Supplier).filter(
            func.lower(func.trim(Supplier.name)) == supplier_name.strip().lower()
        ).first()
        if not supplier:
            supplier = Supplier(name=supplier_name.strip())
            self.session.add(supplier)
            self.session.commit()

        # Znajdź lub utwórz składnik
        ingredient_name_clean = ingredient_name.strip()
        ingredient = self.session.query(Ingredient).filter(
            func.lower(func.trim(Ingredient.name)) == ingredient_name_clean.lower()
        ).first()
        if not ingredient:
            ingredient = Ingredient(
                name=ingredient_name_clean,
                unit_cost=0.0,
                is_special=is_special,
                is_seasonal=is_seasonal,
                season=season
            )
            self.session.add(ingredient)
            self.session.commit()
        else:
            # Jeśli składnik istnieje, aktualizuj właściwości specjalne/sezonowe
            ingredient.is_special = is_special
            ingredient.is_seasonal = is_seasonal
            ingredient.season = season
            self.session.commit()

        # Tworzymy zamówienie
        order = SupplyOrder(supplier_id=supplier.id)
        self.session.add(order)
        self.session.commit()

        order_item = SupplyOrderItem(
            order_id=order.id,
            ingredient_id=ingredient.id,
            quantity=quantity
        )
        self.session.add(order_item)

        # Dodaj składnik do magazynu (InventoryItem) — data ważności 30 dni od dziś
        expiry_date = datetime.utcnow() + timedelta(days=30)
        inventory_item = InventoryItem(
            ingredient_id=ingredient.id,
            quantity=quantity,
            expiry_date=expiry_date
        )
        self.session.add(inventory_item)

        self.session.commit()

        print(
            f"Zamówiono {quantity} jednostek składnika '{ingredient_name_clean}' od dostawcy '{supplier_name.strip()}'.")
        print("Zamówienie zostało złożone i surowiec dodany do magazynu.")


    def receive_supply_order(self, supply_order_id: int, expiry_date: datetime):
        supply_order = self.session.query(SupplyOrder).get(supply_order_id)
        if not supply_order:
            raise ValueError("Zamówienie dostawy nie istnieje.")

        for item in supply_order.items:
            inventory_item = InventoryItem(
                ingredient_id=item.ingredient_id,
                quantity=item.quantity,
                expiry_date=expiry_date
            )
            self.session.add(inventory_item)
        self.session.commit()
        print(f"Przyjęto dostawę zamówienia {supply_order_id} i zaktualizowano zapasy.")

    # 4. Sugestie zamówień
    def suggest_orders(self, threshold=10):
        subquery = (self.session.query(
            InventoryItem.ingredient_id,
            func.sum(InventoryItem.quantity).label("total_quantity")
        )
        .group_by(InventoryItem.ingredient_id)
        .subquery())

        results = (self.session.query(Ingredient, subquery.c.total_quantity)
                   .outerjoin(subquery, Ingredient.id == subquery.c.ingredient_id)
                   .filter((subquery.c.total_quantity.is_(None)) | (subquery.c.total_quantity < threshold))
                   .all())

        suggestions = []
        for ingredient, qty in results:
            suggestions.append((ingredient.name, qty if qty is not None else 0))
        return suggestions

    # 5. Monitorowanie przeterminowanych składników
    def expired_items(self):
        now = datetime.utcnow()
        return (self.session.query(InventoryItem)
                .filter(InventoryItem.expiry_date < now, InventoryItem.quantity > 0)
                .all())

    # 5b. Raport strat przeterminowanych składników
    def expired_items_report(self):
        expired = self.expired_items()
        total_quantity = sum(item.quantity for item in expired)
        total_value = 0.0
        for item in expired:
            price = item.ingredient.unit_cost if hasattr(item.ingredient, 'unit_cost') else 0
            total_value += item.quantity * price
        return {
            "total_expired_items": len(expired),
            "total_quantity_expired": total_quantity,
            "total_value_lost": total_value
        }

    # 6. Zarządzanie składnikami sezonowymi
    def seasonal_ingredients(self, season: str):
        return (self.session.query(Ingredient)
                .filter(Ingredient.is_seasonal == True)
                .filter(func.lower(Ingredient.season) == season.lower())
                .all())

    # 7. Lista dostawców
    def list_suppliers(self):
        return self.session.query(Supplier).all()

    # 8. Historia zamówień
    def order_history(self, limit=50):
        return self.session.query(SupplyOrder).order_by(SupplyOrder.order_date.desc()).limit(limit).all()
