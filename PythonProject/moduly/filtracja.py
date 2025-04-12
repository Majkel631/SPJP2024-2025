def filtruj_trasy(trasy, min_dlugosc=None, max_dlugosc=None, trudnosc=None, region=None):
    return list(filter(lambda trasa: (
        (min_dlugosc is None or float(trasa['dlugosc_km']) >= min_dlugosc) and
        (max_dlugosc is None or float(trasa['dlugosc_km']) <= max_dlugosc) and
        (trudnosc is None or trasa['trudnosc'] == trudnosc) and
        (region is None or trasa['region'] == region)
    ), trasy))
