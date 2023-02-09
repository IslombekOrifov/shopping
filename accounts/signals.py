from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.forms import model_to_dict

from .models import CustomUser, Profile, UserDataOnDeleted
from delivery.models import Delivery


@receiver(pre_delete, sender=CustomUser)
def save_user_data_on_delete(instance, *args, **kwargs):
    deliveries = instance.delivery_set.all()
    discounts = instance.discount_set.all()
    discount_items = instance.discount_items.all()
    orders = instance.orders.all()
    user_data = UserDataOnDeleted.objects.create(
        **model_to_dict(instance, fields=[
            'username',
            'first_name',
            'last_name',
            'email',
            'role,'
        ])
    )
    if deliveries.exists():
        deliveries.update(creator_data_id=user_data.id)
    if discounts.exists():
        discounts.update(creator_data_id=user_data.id)
    if discount_items.exists():
        discount_items.update(creator_data_id=user_data.id)
    if orders.exists():
        orders.update(client_data_id=user_data.id)