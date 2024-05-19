# order/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import Order

@receiver(pre_save, sender=Order)
def pre_save_order(sender, instance, **kwargs):
    ''' To Save TAX_RATE, DISCOUNT_RATE, DISCOUNT_AMOUNT, TOTAL_AMOUNT, Automatically on basis of sub total and rates from .env '''
    instance.calculate_total()