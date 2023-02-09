from django.conf import settings

from general.models import Currency



def upload_avatar_path(instance, image):
    return f'users/{instance.user.username}/vatar/{image}'

def get_default_currency():
    return Currency.objects.get(code=settings.CURRENCY_DEFAULT)


def get_currency(code):
    return Currency.objects.get(code=code)