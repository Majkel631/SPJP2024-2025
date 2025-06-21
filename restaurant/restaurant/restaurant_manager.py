from db.models import Equipment, RestaurantAtmosphere, RestaurantLayout, Table
from db.database import Session
from datetime import datetime

class RestaurantManager:
    def __init__(self):
        self.session = Session()

    # Dodaj sprzęt
    def add_equipment(self, name, eq_type, efficiency=1.0, description=""):
        eq = Equipment(
            name=name,
            type=eq_type,
            efficiency=efficiency,
            condition=100.0,
            description=description
        )
        self.session.add(eq)
        self.session.commit()

    # Zaktualizuj stan sprzętu (zużycie)
    def update_equipment_condition(self, equipment_id, degrade_amount):
        eq = self.session.get(Equipment, equipment_id)
        if eq:
            eq.degrade(degrade_amount)
            eq.last_maintenance = datetime.utcnow()
            self.session.commit()

    # Napraw sprzęt
    def repair_equipment(self, equipment_id):
        eq = self.session.get(Equipment, equipment_id)
        if eq and eq.needs_repair:
            eq.condition = 100.0
            eq.needs_repair = False
            eq.last_maintenance = datetime.utcnow()
            self.session.commit()

    # Dodaj stolik
    def add_table(self, number, seats, location="", description=""):
        table = Table(number=number, seats=seats, location=location, description=description)
        self.session.add(table)
        self.session.commit()

    # Rezerwuj stolik
    def reserve_table(self, table_number):
        table = self.session.query(Table).filter_by(number=table_number).first()
        if table and not table.is_reserved:
            table.is_reserved = True
            self.session.commit()

    # Zwolnij stolik
    def free_table(self, table_number):
        table = self.session.query(Table).filter_by(number=table_number).first()
        if table and table.is_reserved:
            table.is_reserved = False
            self.session.commit()

    # Zmień wystrój / atmosferę
    def set_atmosphere(self, style_name, description="", satisfaction_effect=0.0):
        atmosphere = self.session.query(RestaurantAtmosphere).filter_by(name=style_name).first()
        if not atmosphere:
            atmosphere = RestaurantAtmosphere(
                name=style_name,
                description=description,
                customer_satisfaction_modifier=satisfaction_effect
            )
            self.session.add(atmosphere)
        else:
            atmosphere.description = description
            atmosphere.customer_satisfaction_modifier = satisfaction_effect
        self.session.commit()

    # Dodaj / zmień układ restauracji
    def set_layout(self, layout_name, description=""):
        layout = self.session.query(RestaurantLayout).filter_by(layout_name=layout_name).first()
        if not layout:
            layout = RestaurantLayout(layout_name=layout_name, description=description)
            self.session.add(layout)
        else:
            layout.description = description
        self.session.commit()

    # Pobierz sprzęt
    def get_equipment_list(self):
        return self.session.query(Equipment).all()

    # Pobierz stoliki
    def get_tables(self):
        return self.session.query(Table).all()

    # Pobierz atmosferę
    def get_atmospheres(self):
        return self.session.query(RestaurantAtmosphere).all()

    # Pobierz układ
    def get_layouts(self):
        return self.session.query(RestaurantLayout).all()