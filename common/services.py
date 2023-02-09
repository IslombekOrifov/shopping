from django.db.models import Func, F

def get_price_like_float(price):
    version1 = Func(F(f'{price}'), function='CAST', template = '%(function)s(%(expressions)s AS FLOAT)')
    return version1


