from django.utils import timezone
from django.conf import settings
from datetime import timedelta


class CartItemSessionDeleteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cart = request.session.get(settings.CART_SESSION_ID)
        if cart:
            for key, value in cart.copy().items():
                if timezone.now().timestamp() - value['adding_time'] > settings.CART_SESSION_LIFE_TIME:
                    del cart[key]

        response = self.get_response(request)
        return response