from datetime import date, timedelta
from db.database import Session
from db.models import (
    Restaurant as RestaurantModel,
    Customer as CustomerModel,
    Review,
    MediaCollaboration,
    MarketingCampaign,
    Promotion,
)
class MarketingAndReputationService:
    def __init__(self):
        self.session = Session()

    def get_or_create_restaurant(self) -> RestaurantModel:
        restaurant = self.session.query(RestaurantModel).first()
        if restaurant is None:
            restaurant = RestaurantModel(name="Domyślna Restauracja", reputation_score=0.0)
            self.session.add(restaurant)
            self.session.commit()
            self.session.refresh(restaurant)  # ważne, żeby mieć id
        return restaurant

    def calculate_reputation(self, restaurant: RestaurantModel):
        reviews = self.session.query(Review).filter(Review.restaurant_id == restaurant.id).all()
        media_reviews = self.session.query(MediaCollaboration).filter(
            MediaCollaboration.restaurant_id == restaurant.id).all()

        if not reviews and not media_reviews:
            restaurant.reputation_score = 0.0
        else:
            avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
            media_score = sum(m.review_score for m in media_reviews) / len(media_reviews) if media_reviews else 0
            reputation = (avg_rating * 15 + media_score * 20) / 2
            restaurant.reputation_score = min(100.0, reputation)

        self.session.commit()
        return restaurant.reputation_score

    def run_marketing_campaign(self, campaign_id: int):
        campaign = self.session.get(MarketingCampaign, campaign_id)
        if campaign is None:
            restaurant = self.get_or_create_restaurant()
            # domyślnie tworzymy kampanię na 7 dni
            campaign = MarketingCampaign(
                id=campaign_id,
                restaurant_id=restaurant.id,
                name=f"Kampania {campaign_id}",
                start_date=date.today(),
                end_date=date.today() + timedelta(days=7),
                budget=1000.0,
                reach_score=0.0
            )
            self.session.add(campaign)
            self.session.commit()

        today = date.today()
        if campaign.start_date <= today <= campaign.end_date:
            campaign.reach_score += float(campaign.budget) * 0.1
            self.session.commit()
            return True
        return False

    def apply_promotion(self, customer: CustomerModel, promotion: Promotion):
        today = date.today()
        if promotion.start_date <= today <= promotion.end_date:
            customer.loyalty_points += 5
            self.session.commit()
            return True
        return False

    def submit_review(self, customer: CustomerModel, rating: int, comment: str):
        restaurant = self.get_or_create_restaurant()
        review = Review(
            restaurant_id=restaurant.id,
            customer_id=customer.id,
            rating=rating,
            comment=comment
        )
        self.session.add(review)
        self.session.commit()
        self.calculate_reputation(restaurant)

    def add_loyalty_points(self, customer: CustomerModel, amount_spent: float):
        points = int(amount_spent // 10)
        customer.loyalty_points += points
        self.session.commit()
        return points

    def redeem_loyalty_points(self, customer: CustomerModel, threshold: int = 100):
        if customer.loyalty_points >= threshold:
            customer.loyalty_points -= threshold
            self.session.commit()
            return True
        return False

    def media_review_effect(self, media_id: int):
        media = self.session.get(MediaCollaboration, media_id)
        if media is None:
            restaurant = self.get_or_create_restaurant()
            media = MediaCollaboration(
                id=media_id,
                restaurant_id=restaurant.id,
                media_name="Domyślne Media",
                review_score=5.0
            )
            self.session.add(media)
            self.session.commit()

        restaurant = self.session.get(RestaurantModel, media.restaurant_id)
        if restaurant:
            self.calculate_reputation(restaurant)

    def apply_1promotion(self, customer, promotion):
        pass