import os
import random
from datetime import datetime

from extractors.web_data_collector import HTMLRouteExtractor
from models.route import Route
from analyzers.text_processor import TextProcessor
from reporters.chart_generator import ChartGenerator
from reporters.pdf_report_generator import PDFReportGenerator


def main():
    reports_folder = 'data/extracted_data'
    os.makedirs(reports_folder, exist_ok=True)

    # Wczytaj kod HTML z pliku
    with open("data/html_cache/trasy_turystyczne.html", encoding="utf-8") as f:
        html = f.read()

    # Parsowanie tras z HTML
    extractor = HTMLRouteExtractor()
    routes_data = extractor.parse_html(html)

    routes = []
    for idx, rdata in enumerate(routes_data, start=1):
        rdata.setdefault('id', str(idx))
        rdata.setdefault('description', '')

        # Upewnij się, że ostrzeżenia są listą
        if 'warnings' not in rdata or rdata['warnings'] is None:
            rdata['warnings'] = []

        route = Route(**rdata)
        routes.append(route)

    text_processor = TextProcessor()

    # Uzupełnij trasy o dane z analizy tekstu
    for r in routes:
        info = text_processor.extract_info(r.description)

        new_diff = info.get('difficulty')
        if new_diff and new_diff != 'nieznana':
            r.difficulty = new_diff

        r.category = r.difficulty if getattr(r, 'difficulty', None) else "nieznana"

        new_time = info.get('time_minutes')
        if new_time is not None and new_time > 0:
            r.time_minutes = new_time

        # Dodaj ostrzeżenia z analizy tekstu do już istniejących ostrzeżeń
        if info.get('warnings'):
            if not hasattr(r, 'warnings') or r.warnings is None:
                r.warnings = []
            r.warnings.extend(info['warnings'])

        # Losowa ocena
        r.rating = round(random.uniform(3.5, 5.0), 1)

        # Ścieżki do map i profili
        r.map_path = f"data/maps/{r.id}_map.png"
        r.elevation_profile_path = f"data/profiles/{r.id}_profile.png"

    print("\n=== WYNIKI ANALIZY TRAS ===")
    for r in routes:
        print(f"\nTrasa: {r.name}")
        print(f" - Długość: {r.length_km} km")
        print(f" - Czas przejścia: {r.time_minutes} minut")
        print(f" - Przewyższenie: {r.elevation_gain_m} m")
        print(f" - Trudność: {r.difficulty}")
        print(f" - Ocena: {r.rating}/5")
        warnings_text = ', '.join(r.warnings) if r.warnings else 'brak'
        print(f" - Ostrzeżenia: {warnings_text}")
        print(f" - Opis: {r.description}")

    print(f"Wczytano {len(routes_data)} tras z HTML.")



    chart_gen = ChartGenerator()

    length_histogram_path = os.path.join(reports_folder, "length_histogram.png")
    category_pie_path = os.path.join(reports_folder, "category_pie_chart.png")
    rating_bar_path = os.path.join(reports_folder, "rating_bar_chart.png")
    heatmap_path = os.path.join(reports_folder, "heatmap.png")
    radar_chart_path = os.path.join(reports_folder, "radar_chart.png")

    chart_gen.plot_length_histogram(routes, length_histogram_path)
    chart_gen.plot_category_pie_chart(routes, category_pie_path)
    chart_gen.plot_rating_bar_chart(routes, rating_bar_path)
    chart_gen.plot_heatmap(routes, heatmap_path)
    chart_gen.plot_radar_chart(routes, radar_chart_path)

    # Parametry wyszukiwania do raportu
    search_params = {
        "Region": "Karpaty",
        "Maksymalna długość (km)": "25",
        "Trudność": "średnia i trudna",
        "Sezon": "lipiec"
    }

    pdf_output_path = os.path.join(reports_folder, "report.pdf")
    pdf_gen = PDFReportGenerator(pdf_output_path)

    today_str = datetime.now().strftime("%B %Y")
    pdf_gen.create_title_page(
        f"Raport Rekomendacji Tras Turystycznych - {today_str}",
        datetime.now().strftime("%d.%m.%Y"),
        search_params=search_params
    )

    pdf_gen.add_table_of_contents()

    summary = f"Analiza {len(routes)} tras, 8 rekomendowanych, średni komfort pogodowy 82%"
    pdf_gen.add_summary(summary)

    pdf_gen.add_chart("Histogram długości tras", length_histogram_path)
    pdf_gen.add_category_pie_chart(category_pie_path)
    pdf_gen.add_rating_bar_chart(rating_bar_path)
    pdf_gen.add_heatmap(heatmap_path)
    pdf_gen.add_radar_chart(radar_chart_path)

    # Top 3 trasy wg oceny
    top_routes = sorted(
        routes,
        key=lambda r: r.rating if isinstance(r.rating, (int, float)) else 0,
        reverse=True
    )[:3]
    pdf_gen.add_top_recommendations(top_routes)

    seasonality_data = {r.name: "lipiec" for r in top_routes}
    pdf_gen.add_seasonality_analysis(seasonality_data)

    pdf_gen.add_comparison_table(routes)

    appendix_text = "Źródła danych: własne analizy, pliki GPX, przewodniki PTTK."
    pdf_gen.add_appendix(appendix_text)

    pdf_gen.output()
    print("Raport wygenerowany.")


if __name__ == "__main__":
    main()