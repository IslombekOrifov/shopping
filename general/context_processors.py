from django.conf import settings

from products.models import Category
from general.models import Currency, Contact

def index(request):
    categories = Category.objects.filter(active=True, parent__isnull=True)
    currency_items = Currency.objects.values('code')
    contact = Contact.objects.filter(is_active=True).values('address', 'info_email', 'phone', 'phone2')[:1]
    currency = request.session.get(settings.CURRENCY_SESSION_ID)
    if not currency:
        if request.user.is_authenticated:
            currency = request.session[settings.CURRENCY_SESSION_ID] = request.user.currency.code
        else:
            currency = request.session[settings.CURRENCY_SESSION_ID] = settings.CURRENCY_DEFAULT

    return {'categories': categories, 'currency_items': currency_items, 'currency': currency, 'contact': contact}
    

