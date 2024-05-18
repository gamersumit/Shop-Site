import uuid
from django.db import models
from menu.models import Item
from user.models import ExtendUser
# Create your models here.
      
class Payment(models.Model):
  '''  
  Payment Structure which stores an Payment ID for a user's Order which can be used to fetch and stores order_items.
  It also stores payment deatils at the time of order in the db.
  ID here will be treated as Order ID
 '''  
  PAYMENT_CHOICES = [
        ('CC', 'Credit Card'),
        ('DC', 'Debit Card'),
        ('PP', 'PayPal'),
        ('UPI', 'UPI'),
        ('CASH', 'CASH')
    ]  

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.ForeignKey(ExtendUser, related_name='orders', on_delete=models.CASCADE)
  paid_at = models.DateTimeField(auto_now_add=True)
  payment_type = models.CharField(max_length = 10, choices = PAYMENT_CHOICES)
  sub_total = models.FloatField(null = True, blank=True)
  tax_rate = models.FloatField(default=5.0)
  discount = models.FloatField(null = True, blank=True)
  total = models.FloatField(null = True, blank=True)

  def __str__(self):
    return f"order: {self.id}"


class OrderDetails(models.Model):
    ''' RECORDS ALL OF ITEMS ORDERED BY A USER IN A SINGLE ORDER WITH 
        THE PRICE AT THE TIME OF ORDER AND QANTITY
        Price is not referenced directly from the item table as Price can be updated later
        but we don't want to change the order history price
    '''

    order_id = models.ForeignKey(Payment, related_name='order_details', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='order_items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity}  {self.item_name} for {self.quantity*self.price}"
