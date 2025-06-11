import os
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

class ChartGenerator:
    def plot_length_histogram(self, routes, path):
        lengths = [r.length_km for r in routes if r.length_km is not None]
        plt.figure(figsize=(8, 4))
        plt.hist(lengths, bins=10, color='skyblue', edgecolor='black')
        plt.title("Histogram długości tras")
        plt.xlabel("Długość (km)")
        plt.ylabel("Liczba tras")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path)
        plt.close()

    def plot_category_pie_chart(self, routes, path):
        categories = [r.difficulty for r in routes if hasattr(r, 'difficulty') and r.difficulty]

        if not categories:
            print("Brak kategorii do wygenerowania wykresu kołowego.")
            return

        counter = Counter(categories)
        labels = list(counter.keys())
        sizes = list(counter.values())

        plt.figure(figsize=(10, 10), dpi=300)

        patches, texts, autotexts = plt.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            textprops={'fontsize': 18},
            pctdistance=0.8
        )


        for autotext in autotexts:
            autotext.set_size(20)
            autotext.set_color('white')

        plt.title("Rozkład trudności tras", fontsize=22, pad=20)

        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    def plot_rating_bar_chart(self, routes, path):
        names = [r.name for r in routes if hasattr(r, 'rating')]
        ratings = [r.rating for r in routes if hasattr(r, 'rating')]

        plt.figure(figsize=(18, 9))
        bars = plt.bar(names, ratings, color='orange')

        plt.xticks(rotation=45, ha='right', fontsize=16, fontweight='bold')
        plt.yticks(fontsize=16, fontweight='bold')
        plt.ylabel("Ocena użytkowników", fontsize=18, fontweight='bold')
        plt.title("Wykres ocen użytkowników", fontsize=20, fontweight='bold')
        plt.tight_layout()

        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path)
        plt.close()

    def plot_heatmap(self, routes, path):
        data = np.random.rand(10, 10)
        plt.figure(figsize=(20, 20))
        plt.imshow(data, cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.tight_layout()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path, dpi=200)
        plt.close()

    def plot_radar_chart(self, routes, path):
        labels = ['Długość (km)', 'Trudność', 'Ocena', 'Czas (min)']
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        length_vals = [r.length_km for r in routes if r.length_km is not None]
        length_mean = np.mean(length_vals) if length_vals else 0

        difficulty_map = {'łatwa': 1, 'średnia': 2, 'trudna': 3}
        difficulty_vals = [difficulty_map.get(r.difficulty, 0) for r in routes]
        diff_mean = np.mean([d for d in difficulty_vals if d > 0]) if difficulty_vals else 0

        rating_vals = [r.rating for r in routes if hasattr(r, 'rating')]
        rating_mean = np.mean(rating_vals) if rating_vals else 0

        time_vals = [r.time_minutes for r in routes if hasattr(r, 'time_minutes') and r.time_minutes]
        time_mean = np.mean(time_vals) if time_vals else 0

        values = [length_mean, diff_mean, rating_mean, time_mean]
        values += values[:1]

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

        ax.plot(angles, values, 'o-', linewidth=3, markersize=8, color='navy')
        ax.fill(angles, values, alpha=0.3, color='skyblue')

        ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=16, fontweight='bold', color='darkblue')
        ax.tick_params(axis='y', labelsize=14)  # rozmiar etykiet osi Y
        ax.set_title("Wykres radarowy tras", fontsize=20, fontweight='bold', color='navy', pad=20)
        ax.grid(True, linestyle='--', linewidth=0.7)

        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path)
        plt.close()
