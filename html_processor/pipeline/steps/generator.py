import os
from fpdf import FPDF

from utils.logger import log_error, log_info


def generate_pdf_reports(analyzed_data, output_dir, overwrite=False):
    # Ścieżka do czcionki Unicode (upewnij się, że plik istnieje)
    font_path = os.path.join('assets', 'fonts', 'DejaVuSans.ttf')

    if not os.path.isfile(font_path):
        log_error(f"Missing font file: {font_path}")
        return

    for report in analyzed_data:
        try:
            filename = report['filename'].replace('.html', '') + '_report.pdf'
            output_path = os.path.join(output_dir, filename)

            if os.path.exists(output_path) and not overwrite:
                log_info(f"Skipping existing file (overwrite=False): {output_path}")
                continue

            pdf = FPDF()
            pdf.add_page()

            # Rejestracja i użycie czcionki Unicode
            pdf.add_font('DejaVu', '', font_path, uni=True)
            pdf.set_font('DejaVu', '', 12)

            pdf.cell(0, 10, f"Raport: {report['filename']}", ln=True)
            pdf.ln(5)

            # Nagłówki
            if report['data']:
                headers = report['data'][0].keys()
                pdf.set_font('DejaVu', 'B', 12)
                for header in headers:
                    pdf.cell(40, 10, header, border=1)
                pdf.ln()

                # Dane
                pdf.set_font('DejaVu', '', 12)
                for row in report['data']:
                    for value in row.values():
                        pdf.cell(40, 10, str(value), border=1)
                    pdf.ln()
            else:
                pdf.cell(0, 10, "Brak danych do wyświetlenia", ln=True)

            pdf.output(output_path)
            log_info(f"Successfully generated: {output_path}")

        except Exception as e:
            log_error(f"Failed to generate PDF for {report['filename']}: {e}")