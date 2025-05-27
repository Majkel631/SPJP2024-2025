import os
from bs4 import BeautifulSoup

def parse_html_files(input_dir):
    results = []
    for filename in os.listdir(input_dir):
        if not filename.endswith('.html'):
            continue
        path = os.path.join(input_dir, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                table = soup.find('table')
                if not table:
                    raise ValueError("No table found in HTML")

                rows = table.find_all('tr')
                headers = [th.text.strip() for th in rows[0].find_all('th')]
                records = []
                for row in rows[1:]:
                    cells = [td.text.strip() for td in row.find_all('td')]
                    records.append(dict(zip(headers, cells)))

                results.append({'filename': filename, 'records': records})
        except Exception as e:
            results.append({'filename': filename, 'error': str(e)})
    return results