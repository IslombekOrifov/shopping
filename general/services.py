from django.conf import settings

def get_currency_from_session(request):
    currency = request.session.get(settings.CURRENCY_SESSION_ID)
    if not currency:
        currency = request.session[settings.CURRENCY_SESSION_ID] = settings.CURRENCY_DEFAULT
    return currency

