import os
import re
import numpy as np
from matplotlib import pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle, PageBreak, BaseDocTemplate, PageTemplate, \
    Frame, KeepTogether
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import cm
from reportlab.platypus.tableofcontents import TableOfContents


class PDFReportGenerator:

    def __init__(self, output_path):
        self.output_path = output_path
        self.story = []

        # Czcionki
        font_dir = os.path.join("fonts", "ttf")
        regular = os.path.join(font_dir, "DejaVuSans.ttf")
        bold = os.path.join(font_dir, "DejaVuSans-Bold.ttf")
        italic = os.path.join(font_dir, "DejaVuSans-Oblique.ttf")
        bold_italic = os.path.join(font_dir, "DejaVuSans-BoldOblique.ttf")

        for fpath in [regular, bold, italic]:
            if not os.path.exists(fpath):
                raise FileNotFoundError(f"Nie znaleziono pliku fontu: {fpath}")

        pdfmetrics.registerFont(TTFont("DejaVuSans", regular))
        pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", bold))
        pdfmetrics.registerFont(TTFont("DejaVuSans-Oblique", italic))
        if os.path.exists(bold_italic):
            pdfmetrics.registerFont(TTFont("DejaVuSans-BoldOblique", bold_italic))
            pdfmetrics.registerFontFamily(
                "DejaVuSans",
                normal="DejaVuSans",
                bold="DejaVuSans-Bold",
                italic="DejaVuSans-Oblique",
                boldItalic="DejaVuSans-BoldOblique",
            )
        else:
            pdfmetrics.registerFontFamily(
                "DejaVuSans",
                normal="DejaVuSans",
                bold="DejaVuSans-Bold",
                italic="DejaVuSans-Oblique",
                boldItalic="DejaVuSans-Bold",
            )

        # Style
        self.styles = getSampleStyleSheet()
        for style in self.styles.byName.values():
            style.fontName = "DejaVuSans"

        self.toc = TableOfContents()
        self.toc.levelStyles = [
            ParagraphStyle(fontName='DejaVuSans-Bold', fontSize=14, name='TOCHeading1', leftIndent=20,
                           firstLineIndent=-20, spaceBefore=5),
            ParagraphStyle(fontName='DejaVuSans', fontSize=12, name='TOCHeading2', leftIndent=40, firstLineIndent=-20,
                           spaceBefore=0),
        ]

    def add_section(self, title, text="", level=0):
        anchor_name = re.sub(r'\W+', '_', title)
        heading_style_name = f"Heading{level + 1}"
        if heading_style_name not in self.styles:
            heading_style_name = "Heading1"  # fallback
        heading = Paragraph(f'<a name="{anchor_name}"/>{title}', self.styles[heading_style_name])
        heading._bookmarkName = anchor_name
        heading._level = level
        self.story.append(heading)
        self.story.append(Spacer(1, 0.2 * cm))
        if text:
            self.story.append(Paragraph(text, self.styles["Normal"]))
            self.story.append(Spacer(1, 0.5 * cm))
    def create_title_page(self, title, date, search_params=None):
        title_style = ParagraphStyle(
            name="TitleStyle",
            fontName="DejaVuSans-Bold",
            fontSize=24,
            leading=28,
            alignment=1,
            spaceAfter=12
        )
        date_style = ParagraphStyle(
            name="DateStyle",
            fontName="DejaVuSans",
            fontSize=12,
            leading=16,
            alignment=1,
            spaceAfter=24
        )
        self.story.append(Spacer(1, 5 * cm))
        self.story.append(Paragraph(title, title_style))
        self.story.append(Paragraph(f"Data generowania: {date}", date_style))

        if search_params:
            params_text = ", ".join(f"<b>{k}</b>: {v}" for k, v in search_params.items())
            self.story.append(
                Paragraph(f"Parametry wyszukiwania: {params_text}", self.styles['Normal']))

        self.story.append(PageBreak())

    def add_table_of_contents(self):

        toc_title = "Spis treści"
        anchor_name = re.sub(r'\W+', '_', toc_title)
        toc_heading = Paragraph(f'<a name="{anchor_name}"/>{toc_title}', self.styles["Heading1"])
        toc_heading._bookmarkName = anchor_name
        toc_heading._level = None
        self.story.append(toc_heading)
        self.story.append(Spacer(1, 0.5 * cm))
        self.story.append(self.toc)
        self.story.append(PageBreak())

    def add_seasonality_analysis(self, seasonality_data):
        self.add_section("Analiza sezonowości", level=0)
        for route_name, best_month in seasonality_data.items():
            self.story.append(Paragraph(f"<b>{route_name}</b>: najlepszy miesiąc — {best_month}", self.styles["Normal"]))
            self.story.append(Spacer(1, 0.3 * cm))
        self.story.append(Spacer(1, 1 * cm))

    def add_summary(self, text):
        self.add_section("Podsumowanie wykonawcze", text, level=0)

    def add_top_recommendations(self, top_routes):
        self.story.append(Paragraph("<b>Top 3 rekomendacje:</b>", self.styles["Heading2"]))
        self.story.append(Spacer(1, 0.5 * cm))
        for route in top_routes:
            self.story.append(Paragraph(f"<b>{route.name}</b>", self.styles["Heading3"]))

            time_text = "nieznany czas"
            try:
                time_val = int(route.time_minutes)
                if time_val > 0:
                    time_text = f"{time_val} min"
            except Exception as e:
                print(f"[ERROR] converting time_minutes: {e}")

            difficulty_text = route.difficulty if route.difficulty else "nieznana trudność"

            self.story.append(Paragraph(f"Czas: {time_text} | Trudność: {difficulty_text}", self.styles["Normal"]))
            self.story.append(Spacer(1, 0.3 * cm))

            if hasattr(route, 'map_path') and route.map_path and os.path.exists(route.map_path):
                self.story.append(Image(route.map_path, width=8 * cm, height=6 * cm))
            if hasattr(route, 'elevation_profile_path') and route.elevation_profile_path and os.path.exists(
                    route.elevation_profile_path):
                self.story.append(Image(route.elevation_profile_path, width=8 * cm, height=6 * cm))
            self.story.append(Spacer(1, 1 * cm))

    def add_chart(self, title, chart_path):
        if os.path.exists(chart_path):
            self.add_section(title, level=0)
            self.story.append(Image(chart_path, width=16 * cm, height=8 * cm))
            self.story.append(Spacer(1, 1 * cm))

    def add_comparison_table(self, routes):
        self.add_section("Tabela zbiorcza tras", level=0)
        data = [["Nazwa", "Długość (km)", "Czas (min)", "Trudność", "Ostrzeżenia"]]
        for r in routes:
            length_text = f"{r.length_km:.1f}" if r.length_km is not None else "nieznana"
            time_text = str(r.time_minutes) if r.time_minutes is not None else "nieznany"
            difficulty_text = r.difficulty if r.difficulty else "nieznana"
            warnings_text = ', '.join(r.warnings) if r.warnings else "brak"
            data.append([r.name, length_text, time_text, difficulty_text, warnings_text])

        table = Table(data, colWidths=[6 * cm, 2.5 * cm, 2.5 * cm, 3 * cm, 6 * cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ]))
        self.story.append(table)
        self.story.append(Spacer(1, 1 * cm))

    def add_appendix(self, appendix_text):
        self.add_section("Aneks – dane źródłowe", appendix_text, level=0)

    def add_category_pie_chart(self, path):
        self.add_section("Wykres kołowy kategorii tras", level=0)
        if os.path.exists(path):
            self.story.append(Image(path, width=16 * cm, height=8 * cm))
        else:
            self.story.append(Paragraph("Brak wykresu – plik nie został znaleziony.", self.styles['Normal']))
        self.story.append(Spacer(1, 1 * cm))

    def add_rating_bar_chart(self, path):
        self.add_section("Wykres ocen użytkowników", level=0)
        if os.path.exists(path):
            self.story.append(Image(path, width=16 * cm, height=8 * cm))
        else:
            self.story.append(Paragraph("Brak wykresu – plik nie został znaleziony.", self.styles['Normal']))
        self.story.append(Spacer(1, 1 * cm))

    def add_heatmap(self, path):
        self.add_section("Mapa ciepła dostępności tras", level=0)
        if os.path.exists(path):
            print(f"Usuwam istniejący plik mapy: {path}")
            os.remove(path)

        # Dane do mapy cieplnej
        months = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
                  'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień']
        x_labels = ['Trasa 1', 'Trasa 2', 'Trasa 3', 'Trasa 4', 'Trasa 5',
                    'Trasa 6', 'Trasa 7', 'Trasa 8', 'Trasa 9']

        data = np.random.rand(12, 9)

        print(f"Generuję mapę i zapisuję do: {path}")

        fig, ax = plt.subplots(figsize=(10, 6))
        heatmap = ax.imshow(data, cmap='hot')

        ax.set_yticks(np.arange(len(months)))
        ax.set_yticklabels([f"{i + 1} {m}" for i, m in enumerate(months)])

        ax.set_xticks(np.arange(len(x_labels)))
        ax.set_xticklabels(x_labels, rotation=45, ha='right')

        ax.set_title("Mapa ciepła dostępności tras w poszczególnych miesiącach")
        ax.set_xlabel("Trasy")
        ax.set_ylabel("Miesiące")

        plt.colorbar(heatmap)
        plt.tight_layout()

        plt.savefig(path, format='png')
        plt.close()
        img_width = 16 * cm
        img_height = img_width * (6 / 10)

        self.story.append(Image(path, width=img_width, height=img_height))
        self.story.append(Spacer(1, 1 * cm))

    def add_radar_chart(self, path):
        self.add_section("Wykres radarowy tras", level=0)
        if os.path.exists(path):
            self.story.append(Image(path, width=16 * cm, height=8 * cm))
        else:
            self.story.append(Paragraph("Brak wykresu – plik nie został znaleziony.", self.styles['Normal']))
        self.story.append(Spacer(1, 1 * cm))

    def output(self):
        def add_page_number(canvas, doc):
            page_num_text = f"Strona {doc.page}"
            canvas.setFont("DejaVuSans", 9)
            canvas.drawRightString(A4[0] - 2 * cm, 1 * cm, page_num_text)

        class MyDocTemplate(BaseDocTemplate):
            def afterFlowable(self, flowable):
                if isinstance(flowable, Paragraph) and hasattr(flowable, '_bookmarkName'):
                    text = flowable.getPlainText().strip()
                    level = getattr(flowable, '_level', None)
                    if text and isinstance(level, int):
                        self.notify('TOCEntry', (level, text, self.page))

        doc = MyDocTemplate(
            self.output_path,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm
        )

        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
        template = PageTemplate(id='main', frames=frame, onPage=add_page_number)
        doc.addPageTemplates([template])
        doc.multiBuild(self.story)