from typing import List, Dict, Counter


def analyze_reviews(self, reviews: List[str]) -> Dict:
    sentiments = {'positive': 0, 'negative': 0}
    ratings = []
    aspects_counter = Counter()
    dates = []

    for review in reviews:
        text = review.lower()

        # Sentyment
        if any(word in text for word in self.POSITIVE_WORDS):
            sentiments['positive'] += 1
        if any(word in text for word in self.NEGATIVE_WORDS):
            sentiments['negative'] += 1

        # Oceny
        rating_match = self.RATING_PATTERN.search(review)
        if rating_match:
            if rating_match.group(1):
                ratings.append(float(rating_match.group(1)))
            elif rating_match.group(2):
                ratings.append(float(rating_match.group(2)) / 2)  # z 10 na 5
            elif rating_match.group(3):
                ratings.append(len(rating_match.group(3)))

        # Aspekty
        for aspect in self.ASPECTS:
            if aspect in text:
                aspects_counter[aspect] += 1

        # Daty
        for date_match in self.DATE_PATTERN.finditer(review):
            day, month, year = date_match.groups()
            if len(year) == 2:
                year = '20' + year  # prosta normalizacja roku
            dates.append(f"{day.zfill(2)}-{month.zfill(2)}-{year}")

    average_rating = sum(ratings) / len(ratings) if ratings else 0

    return {
        'positive_reviews': sentiments['positive'],
        'negative_reviews': sentiments['negative'],
        'average_rating': average_rating,
        'most_mentioned_aspects': aspects_counter.most_common(),
        'dates': dates
    }