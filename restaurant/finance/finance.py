from datetime import datetime, timedelta

from sqlalchemy import func

from db.database import Session
from db.models import Order, Ingredient, StaffMember, FinancialTransaction, Budget, FinancialTransactionType


class FinanceManager:
    LOW_BALANCE_THRESHOLD = 500.0  # Próg alarmowy dla budżetu

    def __init__(self):
        self.session = Session()
        budget = self.session.query(Budget).first()
        if not budget:
            budget = Budget(current_balance=0.0, warning_threshold=1000.0)
            self.session.add(budget)
            self.session.commit()
    # 1. Dodanie transakcji (przychód lub wydatek)
    def record_transaction(self, amount, type_, description="", related_order_id=None, related_staff_id=None):
        transaction = FinancialTransaction(
            amount=amount,
            type=type_,
            description=description,
            related_order_id=related_order_id,
            related_staff_id=related_staff_id,
            timestamp=datetime.utcnow()
        )
        self.session.add(transaction)

        # Aktualizacja budżetu
        budget = self.session.query(Budget).first()
        if budget:
            budget.current_balance += amount

        self.session.commit()
        self._check_low_balance()

    # 2. Wypłata pensji wszystkim pracownikom
    def pay_salaries(self):
        staff_members = self.session.query(StaffMember).all()
        for member in staff_members:
            self.record_transaction(
                amount=-member.salary,
                type_=FinancialTransactionType.SALARY,
                description=f"Wypłata pensji dla {member.name}",
                related_staff_id=member.id
            )

    # 3. Opłata za czynsz
    def pay_rent(self, amount):
        self.record_transaction(
            amount=-amount,
            type_=FinancialTransactionType.RENT,
            description="Opłata za czynsz"
        )

    # 4. Opłata za sprzęt
    def purchase_equipment(self, amount, description="Zakup sprzętu"):
        self.record_transaction(
            amount=-amount,
            type_=FinancialTransactionType.EQUIPMENT,
            description=description
        )

    # 5. Naliczanie podatku
    def charge_tax(self, amount):
        self.record_transaction(
            amount=-amount,
            type_=FinancialTransactionType.TAX,
            description="Opłata podatkowa"
        )

    # 6. Pobranie raportu przychodów i wydatków
    def get_financial_report(self, period="daily"):
        now = datetime.utcnow()
        if period == "daily":
            since = now - timedelta(days=1)
        elif period == "weekly":
            since = now - timedelta(weeks=1)
        elif period == "monthly":
            since = now - timedelta(days=30)
        else:
            raise ValueError("Okres może być tylko: 'daily', 'weekly', 'monthly'.")

        transactions = self.session.query(FinancialTransaction).filter(
            FinancialTransaction.timestamp >= since
        ).all()

        income = sum(t.amount for t in transactions if t.amount > 0)
        expenses = sum(-t.amount for t in transactions if t.amount < 0)
        net = income - expenses

        return {
            "period": period,
            "income": income,
            "expenses": expenses,
            "net_profit": net
        }

    # 7. Prognoza przyszłych zysków/strat (na podstawie średniej z ostatniego miesiąca)
    def forecast_next_month(self):
        now = datetime.utcnow()
        since = now - timedelta(days=30)

        transactions = self.session.query(FinancialTransaction).filter(
            FinancialTransaction.timestamp >= since
        ).all()

        daily_net = []
        for i in range(30):
            day = now - timedelta(days=i)
            day_transactions = [t.amount for t in transactions if t.timestamp.date() == day.date()]
            daily_net.append(sum(day_transactions))

        avg_daily_profit = sum(daily_net) / 30
        forecast = avg_daily_profit * 30

        return {
            "avg_daily_profit": avg_daily_profit,
            "forecast_next_month": forecast
        }

    # 8. Sprawdzenie budżetu i alarm
    def _check_low_balance(self):
        budget = self.session.query(Budget).first()
        if budget and budget.current_balance < self.LOW_BALANCE_THRESHOLD:
            print("  Uwaga: niski stan budżetu!")

    # 9. Pobranie stanu konta
    def get_budget_balance(self):
        budget = self.session.query(Budget).first()
        return budget.current_balance if budget else None

    # 10. Zaciągnięcie kredytu
    def take_loan(self, amount, description="Kredyt inwestycyjny"):
        self.record_transaction(
            amount=amount,
            type_=FinancialTransactionType.LOAN,
            description=description
        )