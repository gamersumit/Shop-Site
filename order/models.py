import uuid
from django.db import models
from menu.models import Item
from user.models import ExtendUser
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from decimal import Decimal
# Create your models here.
      
class Order(models.Model):
  """ Generates a Order ID which is referenced with user """

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.ForeignKey(ExtendUser, related_name='order', on_delete=models.CASCADE)
  ordered_at = models.DateTimeField(auto_now_add=True)
  
  subtotal_amount = models.DecimalField(max_digits=10, decimal_places=2)
  tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
  tax_rate = models.DecimalField(max_digits=6, decimal_places=2)
  discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  discount_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
  total_amount = models.DecimalField(max_digits=10, decimal_places=2)
 
  def calculate_total(self):
    self.tax_rate = Decimal(settings.TAX_RATE)
    self.discount_rate = Decimal(settings.DISCOUNT_RATE)
    
    self.tax_amount = (self.subtotal_amount * self.tax_rate) / Decimal(100)
    self.discount_amount = (self.subtotal_amount * self.discount_rate) / Decimal(100.0)
    self.total_amount = self.subtotal_amount + self.tax_amount - self.discount_amount

    
  def __str__(self):
    return f"order_id: {self.id}"



class OrderItems(models.Model):
    ''' 
        RECORDS ALL OF ITEMS ORDERED BY A USER IN A SINGLE ORDER WITH 
        THE PRICE AT THE TIME OF ORDER AND QANTITY
        Price is not referenced directly from the item table as Price can be updated later
        but we don't want to change the order history price
    '''

    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='order_items', on_delete=models.CASCADE)
    price = models.IntegerField() # quantity * price per unit
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity}  {self.item.name} for {self.quantity*self.price}"
