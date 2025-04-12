from functools import reduce

def srednia_temp(pogoda):
    temp = list(map(lambda d: float(d['temp_srednia']), pogoda))
    return sum(temp) / len(temp) if temp else 0

def suma_opadow(pogoda):
    return reduce(lambda a, b: a + float(b['opady']), pogoda, 0)

def liczba_dni_slonecznych(pogoda, prog=20.0):
    return len(list(filter(lambda d: float(d['temp_srednia']) > prog and float(d['zachmurzenie']) < 30, pogoda)))
