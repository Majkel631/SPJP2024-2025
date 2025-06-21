import enum
from sqlalchemy import Date

from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime,
    ForeignKey, Enum, Boolean, Table, Text, DECIMAL
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# Tabela asocjacyjna między MenuItem a Ingredient z dodatkową kolumną quantity
menuitem_ingredients = Table(
    "menuitem_ingredients",
    Base.metadata,
    Column("menu_item_id", Integer, ForeignKey("menu_items.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id"), primary_key=True),
    Column("quantity", Float, nullable=False)
)


class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    category = Column(Enum("Starter", "Main", "Dessert", "Drink", name="menu_category"), nullable=False)
    price = Column(Float, nullable=False)
    is_special = Column(Boolean, default=False)

    recipe = relationship("Recipe", uselist=False, back_populates="menu_item", cascade="all, delete-orphan")
    orders = relationship("OrderItem", back_populates="menu_item")
    ingredients = relationship(
        "Ingredient",
        secondary=menuitem_ingredients,
        back_populates="menu_items"
    )


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False, unique=True)

    menu_item = relationship("MenuItem", back_populates="recipe")
    ingredient_usages = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    unit_cost = Column(Float, nullable=False)  # koszt za jednostkę

    # Dodatkowe pola do zarządzania sezonowością
    is_seasonal = Column(Boolean, default=False, nullable=False)
    season = Column(String(50), nullable=True)  # np. 'Lato', 'Zima', 'Jesień', 'Wiosna'
    is_special = Column(Boolean, default=False)  # <-- nowe pole
    is_seasonal = Column(Boolean, default=False)  # <-- nowe pole
    season = Column(String, nullable=True)
    # Relacje
    inventory_items = relationship(
        "InventoryItem",
        back_populates="ingredient",
        cascade="all, delete-orphan"
    )
    recipe_usages = relationship(
        "RecipeIngredient",
        back_populates="ingredient"
    )
    menu_items = relationship(
        "MenuItem",
        secondary="menuitem_ingredients",  # jeśli to jest nazwa tabeli asocjacyjnej
        back_populates="ingredients"
    )


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    quantity = Column(Float, nullable=False)

    recipe = relationship("Recipe", back_populates="ingredient_usages")
    ingredient = relationship("Ingredient", back_populates="recipe_usages")


class InventoryItem(Base):
    __tablename__ = "inventory_items"
    id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    expiry_date = Column(DateTime, nullable=False)

    ingredient = relationship("Ingredient", back_populates="inventory_items")


class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact_info = Column(String(100))

    # Zamówienia surowców od dostawcy
    supply_orders = relationship("SupplyOrder", back_populates="supplier")

    def __repr__(self):
        return f"<Supplier(id={self.id}, name='{self.name}')>"


class SupplyOrder(Base):
    __tablename__ = "supply_orders"
    id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    order_date = Column(DateTime, default=datetime.utcnow)  # poprawione

    supplier = relationship("Supplier", back_populates="supply_orders")
    items = relationship("SupplyOrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SupplyOrder(id={self.id}, supplier_id={self.supplier_id}, order_date={self.order_date})>"



class SupplyOrderItem(Base):
    __tablename__ = "supply_order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("supply_orders.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    quantity = Column(Float, nullable=False)

    order = relationship("SupplyOrder", back_populates="items")
    ingredient = relationship("Ingredient")

    def __repr__(self):
        return f"<SupplyOrderItem(id={self.id}, order_id={self.order_id}, ingredient_id={self.ingredient_id}, quantity={self.quantity})>"


# noinspection PyDeprecation
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)  # poprawione

    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)

    supplier = relationship("Supplier", back_populates="orders", foreign_keys=[supplier_id])
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    total_price = Column(Float, default=0.0)

    def __repr__(self):
        return f"<Order(id={self.id}, supplier_id={self.supplier_id}, timestamp={self.timestamp})>"


Supplier.orders = relationship("Order", back_populates="supplier")


class OrderItem(Base):
    __tablename__ = "order_items"
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), primary_key=True)
    quantity = Column(Integer, default=1)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="orders")

    def __repr__(self):
        return f"<OrderItem(order_id={self.order_id}, menu_item_id={self.menu_item_id}, quantity={self.quantity})>"





class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    budget = Column(Float, default=50.0)
    preference = Column(String(100))
    loyalty_points = Column(Integer, default=0)
    reviews = relationship("Review", back_populates="customer")


class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    reputation_score = Column(Float, default=0.0)
    reviews = relationship("Review", back_populates="restaurant")
    campaigns = relationship("MarketingCampaign", back_populates="restaurant")
    promotions = relationship("Promotion", back_populates="restaurant")


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    rating = Column(Integer)  # 1–5
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    restaurant = relationship("Restaurant", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")


class MarketingCampaign(Base):
    __tablename__ = "marketing_campaigns"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    name = Column(String(255))
    budget = Column(DECIMAL(10, 2))
    start_date = Column(Date)
    end_date = Column(Date)
    reach_score = Column(Float, default=0.0)

    restaurant = relationship("Restaurant", back_populates="campaigns")


class Promotion(Base):
    __tablename__ = "promotions"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    title = Column(String(255))
    description = Column(Text)
    discount_percent = Column(Float)
    start_date = Column(Date)
    end_date = Column(Date)

    restaurant = relationship("Restaurant", back_populates="promotions")


class MediaCollaboration(Base):
    __tablename__ = "media_collaborations"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    media_name = Column(String(255))
    review_score = Column(Float)
    date = Column(Date)
    notes = Column(Text)

    restaurant = relationship("Restaurant")









class StaffMember(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    role = Column(Enum("Chef", "Waiter", "Bartender", name="staff_roles"), nullable=False)
    skill = Column(Float, default=1.0)
    salary = Column(Float, default=100.0)
    is_available = Column(Boolean, default=True)

    performance = Column(Float, default=1.0)
    satisfaction = Column(Float, default=5.0)
    assigned_shift = Column(String(50), default="Brak")
    assigned_task = Column(Text, default="Brak")
    trainings_completed = Column(Integer, default=0)


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    reservation_time = Column(DateTime, nullable=False)
    table_number = Column(Integer, nullable=False)

    customer = relationship("Customer", back_populates="reservations")


class WaitQueue(Base):
    __tablename__ = "wait_queue"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    arrival_time = Column(DateTime, nullable=False)

    customer = relationship("Customer", back_populates="wait_queue_entries")


# Relacje w modelu Customer
Customer.reservations = relationship("Reservation", back_populates="customer", cascade="all, delete-orphan")
Customer.wait_queue_entries = relationship("WaitQueue", back_populates="customer", cascade="all, delete-orphan")




class FinancialTransactionType(enum.Enum):
    INCOME = "Income"
    EXPENSE = "Expense"
    LOAN = "Loan"
    TAX = "Tax"
    SALARY = "Salary"
    RENT = "Rent"
    EQUIPMENT = "Equipment"
    OTHER = "Other"


class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float, nullable=False)
    type = Column(Enum(FinancialTransactionType), nullable=False)
    description = Column(Text)
    related_order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    related_staff_id = Column(Integer, ForeignKey("staff.id"), nullable=True)

    order = relationship("Order", backref="financial_transactions")
    staff_member = relationship("StaffMember", backref="financial_transactions")


class Budget(Base):
    __tablename__ = "budget"

    id = Column(Integer, primary_key=True)
    current_balance = Column(Float, default=0.0)
    warning_threshold = Column(Float, default=1000.0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)  # np. 0.05 = 5%
    start_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    paid_amount = Column(Float, default=0.0)
    description = Column(Text)

    def remaining_balance(self):
        return self.amount + (self.amount * self.interest_rate) - self.paid_amount


class FixedCostType(enum.Enum):
    RENT = "Rent"
    TAX = "Tax"
    MAINTENANCE = "Maintenance"
    OTHER = "Other"


class FixedCost(Base):
    __tablename__ = "fixed_costs"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum(FixedCostType), nullable=False)
    amount = Column(Float, nullable=False)
    cycle = Column(String(20), default="monthly")  # np. "daily", "weekly", "monthly"
    last_paid = Column(DateTime, default=datetime.utcnow)


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    efficiency = Column(Float, default=1.0)
    condition = Column(Float, default=100.0)
    description = Column(String)
    needs_repair = Column(Boolean, default=False)
    last_maintenance = Column(DateTime, default=datetime.utcnow)

    def degrade(self, amount):
        self.condition = max(0.0, self.condition - amount)
        if self.condition < 40:
            self.needs_repair = True


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True)
    seats = Column(Integer)
    location = Column(String)  # np. "okno", "centrum", "taras"
    is_reserved = Column(Boolean, default=False)
    description = Column(String, nullable=True)


class RestaurantAtmosphere(Base):
    __tablename__ = "restaurant_atmosphere"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # np. "Elegancka", "Przytulna", "Nowoczesna"
    description = Column(String)
    customer_satisfaction_modifier = Column(Float, default=1.0)


class RestaurantLayout(Base):
    __tablename__ = "restaurant_layout"

    id = Column(Integer, primary_key=True)
    layout_name = Column(String, nullable=False)
    description = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)