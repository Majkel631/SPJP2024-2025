from random import random

from db.database import Session
from db.models import StaffMember

class StaffManager:
    def __init__(self):
        self.session = Session()

    def add_staff(self, name, role, salary=100.0, skill=1.0):
        new_staff = StaffMember(name=name, role=role, skill=skill, salary=salary)
        self.session.add(new_staff)
        self.session.commit()

    def delete_staff(self, employee_id):
        staff = self.session.query(StaffMember).filter_by(id=employee_id).first()
        if staff:
            self.session.delete(staff)
            self.session.commit()
        else:
            raise ValueError(f"Nie znaleziono pracownika o ID {employee_id}")

    def edit_staff(self, employee_id, name=None, role=None, salary=None):
        staff = self.session.query(StaffMember).filter_by(id=employee_id).first()
        if not staff:
            raise ValueError(f"Nie znaleziono pracownika o ID {employee_id}")
        if name:
            staff.name = name
        if role:
            staff.role = role
        if salary is not None:
            staff.salary = salary
        self.session.commit()

    def list_staff(self):
        return self.session.query(StaffMember).all()

  # 1. Przydzielanie do zmian (zakładam pole shifts jako lista stringów)
    def assign_shift(self, employee_id, shift):
        staff = self.session.query(StaffMember).filter_by(id=employee_id).first()
        if not staff:
            raise ValueError(f"Nie znaleziono pracownika o ID {employee_id}")
        if not hasattr(staff, 'shifts'):
            staff.shifts = []
        staff.shifts.append(shift)
        self.session.commit()

    # 2. Wpływ umiejętności na jakość - ocena jakości (przykład)
    def evaluate_quality(self, employee_id):
        staff = self.session.query(StaffMember).filter_by(id=employee_id).first()
        if not staff:
            raise ValueError(f"Nie znaleziono pracownika o ID {employee_id}")
        # Prosty model: jakość = skill * losowy współczynnik (0.8 - 1.2)
        quality = staff.skill * (0.8 + 0.4 * random())
        return quality

    # 3. Zarządzanie premiami
    def grant_bonus(self, employee_id, amount):
        staff = self.session.query(StaffMember).filter_by(id=employee_id).first()
        if not staff:
            raise ValueError(f"Nie znaleziono pracownika o ID {employee_id}")
        staff.salary += amount
        self.session.commit()

    # 4. Rozwój i szkolenia (zwiększenie umiejętności)
    def train_staff(self, employee_id, skill_increase):
        staff = self.session.query(StaffMember).filter_by(id=employee_id).first()
        if not staff:
            raise ValueError(f"Nie znaleziono pracownika o ID {employee_id}")
        staff.skill += skill_increase
        if staff.skill > 10:
            staff.skill = 10  # Maksymalny poziom umiejętności
        self.session.commit()

    # 5. Monitorowanie wydajności
    def update_performance(self, employee_id, performance_score):
        staff = self.session.query(StaffMember).filter_by(id=employee_id).first()
        if not staff:
            raise ValueError(f"Nie znaleziono pracownika o ID {employee_id}")
        staff.performance_score = performance_score
        self.session.commit()

    # 6. Monitorowanie zadowolenia personelu
    def update_satisfaction(self, employee_id, satisfaction_level):
        staff = self.session.query(StaffMember).filter_by(id=employee_id).first()
        if not staff:
            raise ValueError(f"Nie znaleziono pracownika o ID {employee_id}")
        staff.satisfaction_level = satisfaction_level
        self.session.commit()


