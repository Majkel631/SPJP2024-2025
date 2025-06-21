from datetime import datetime, timedelta
from db.database import Session
from db.models import Customer as CustomerModel, MenuItem, Reservation, WaitQueue
import random


class Customer:

    def __init__(self):
        self.session = Session()


    def get_by_id(self, customer_id):
        return self.session.query(CustomerModel).filter_by(id=customer_id).first()

    def choose_item(self, menu_items):
        return menu_items[0] if menu_items else None

    def list_customers(self):
        customers = self.session.query(CustomerModel).all()
        return [
            {
                "id": c.id,
                "budget": c.budget,
                "preferred_category": c.preference
            }
            for c in customers
        ]

    def simulate_queue_and_reservations(self):
        customers = self.session.query(CustomerModel).all()
        if not customers:
            print("Brak klientów w bazie.")
            return


        self.session.query(WaitQueue).delete()
        self.session.query(Reservation).delete()
        self.session.commit()


        queue_customers = random.sample(customers, min(10, len(customers)))

        for c in queue_customers:
            wait_entry = WaitQueue(customer_id=c.id,
                                   arrival_time=datetime.now() - timedelta(minutes=random.randint(0, 30)))
            self.session.add(wait_entry)


        remaining_customers = [c for c in customers if c not in queue_customers]
        reservation_customers = random.sample(remaining_customers, min(5, len(remaining_customers)))

        for c in reservation_customers:
            reservation_time = datetime.now() + timedelta(hours=random.randint(1, 5))
            table_number = random.randint(1, 20)
            reservation = Reservation(customer_id=c.id, reservation_time=reservation_time, table_number=table_number)
            self.session.add(reservation)

        self.session.commit()

        print("\nKolejka klientów:")
        for c in queue_customers:
            print(f" - Klient ID={c.id}, budżet={c.budget:.2f}, preferencja={c.preference}")

        print("\nRezerwacje:")
        for c in reservation_customers:
            print(
                f" * Klient ID={c.id}, rezerwacja na stolik {table_number} o {reservation_time.strftime('%Y-%m-%d %H:%M')}")
    def delete_customer(self, customer_id):
        customer = self.session.query(CustomerModel).filter_by(id=customer_id).first()
        if not customer:
            raise ValueError("Nie znaleziono klienta o podanym ID.")
        self.session.delete(customer)
        self.session.commit()

    def evaluate_customer_satisfaction(self):
        customers = self.session.query(CustomerModel).all()
        menu_items = self.session.query(MenuItem).all()

        results = []
        for customer in customers:
            preferred_dishes = [item for item in menu_items if item.category == customer.preference]

            if not preferred_dishes:
                satisfaction = random.randint(2, 3)
            else:
                avg_price = sum(item.price for item in preferred_dishes) / len(preferred_dishes)
                num_dishes = len(preferred_dishes)

                dishes_score = min(3, max(1, num_dishes))
                budget_ratio = customer.budget / avg_price if avg_price > 0 else 0
                budget_score = 2 if budget_ratio >= 1.2 else 1
                random_score = random.randint(0, 1)

                satisfaction = min(5, dishes_score + budget_score + random_score)

            results.append({"id": customer.id, "satisfaction": satisfaction})

        return results

    def simulate_customers(self, count):
        categories = ['Starter', 'Main', 'Dessert', 'Drink']
        now = datetime.now()
        hour = now.hour

        for _ in range(count):
            if 6 <= hour < 11:
                time_of_day = 'breakfast'
            elif 11 <= hour < 15:
                time_of_day = 'lunch'
            elif 15 <= hour < 18:
                time_of_day = 'afternoon'
            elif 18 <= hour < 22:
                time_of_day = 'dinner'
            else:
                time_of_day = 'late'

            budget = round(random.uniform(10, 150), 2)
            if time_of_day == 'dinner':
                budget *= 1.3
            elif time_of_day == 'breakfast':
                budget *= 0.7

            preference = random.choices(
                population=categories,
                weights=[0.2, 0.4, 0.2, 0.2],
                k=1
            )[0]

            customer = CustomerModel(budget=budget, preference=preference)
            self.session.add(customer)

        self.session.commit()

    def add_customer(self, budget, preference):
        customer = CustomerModel(budget=budget, preference=preference)
        self.session.add(customer)
        self.session.commit()
        print(f"Dodano klienta ID={customer.id} z budżetem {budget} i preferencją {preference}")

    def choose_item_advanced(self, customer, menu_items):
        """Wybiera danie uwzględniając budżet, preferencje i popularność"""
        filtered_items = [item for item in menu_items if
                          item.category == customer.preference and item.price <= customer.budget]
        if not filtered_items:
            return None


        scored_items = []
        for item in filtered_items:
            popularity = getattr(item, 'popularity', 0)
            price_factor = 1 / item.price if item.price > 0 else 0
            score = popularity * 2 + price_factor
            scored_items.append((score, item))

        scored_items.sort(key=lambda x: x[0], reverse=True)
        return scored_items[0][1]

    def random_customer_event(self, customer_id):
        events = [
            ("complaint", "Skarga na długie oczekiwanie."),
            ("praise", "Pochwała za smaczne jedzenie."),
            ("special", "Specjalna okazja: urodziny klienta!"),
            ("neutral", "Brak zdarzeń.")
        ]
        event = random.choices(events, weights=[0.1, 0.2, 0.05, 0.65], k=1)[0]

        print(f"Klient ID={customer_id} - zdarzenie: {event[1]}")
        return event

    def make_reservation(self, customer_id, datetime_obj, table_number):
        reservation = Reservation(
            customer_id=customer_id,
            reservation_time=datetime_obj,
            table_number=table_number
        )
        self.session.add(reservation)
        self.session.commit()
        print(f"Rezerwacja dla klienta {customer_id} na stolik {table_number} o {datetime_obj} została utworzona.")

    def get_queue(self):
        queue = self.session.query(WaitQueue).order_by(WaitQueue.arrival_time).all()
        return queue