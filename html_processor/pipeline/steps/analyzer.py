def analyze_data(file_data, options=None):
    options = options or {}
    records = file_data['records']

    # Dummy implementation: add totals if requested
    if options.get('calculate_totals'):
        for record in records:
            try:
                record['Wartość'] = float(record['Ilość']) * float(record['Cena'])
            except:
                continue

    return records
