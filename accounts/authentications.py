from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .models import CustomUser


UserModel = get_user_model()


class EmailAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            email = kwargs.get(CustomUser.EMAIL_FIELD)
        if username is None or password is None:
            return
        try:
            email = username
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            CustomUser().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user