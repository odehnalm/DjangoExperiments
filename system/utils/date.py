from datetime import datetime, timedelta
from calendar import monthrange

# Inspired from here http://stackoverflow.com/questions/7015587/python-difference-of-2-datetimes-in-months
def monthdelta(d1,d2):
    """Función importante para calcular la diferencia de meses entre dos fechas, ojo d2>d1
    """
    delta = 0
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += timedelta(days=mdays)
        if d1 <= d2:
            delta += 1
        else:
            break
    # use with df['months_difference'] = df[['date1', 'date2']].apply(monthdelta, axis=1)
    return delta