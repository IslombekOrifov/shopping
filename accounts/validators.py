from django.core.exceptions import ValidationError

from .models import CustomUser


def is_client(user_id):
    role = CustomUser.objects.get(pk=user_id).role
    if role != CustomUser.CHOICE_ROLE[0][0]:
        raise ValidationError('Adminlarga mumkin emas!')
    

