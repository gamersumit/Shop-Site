from turtle import back
import uuid
from django.db import models
import uuid
from menu.models import Item
from user.models import ExtendUser
# Create your models here.
      
class Cart(models.Model):
  ''' Add Product/Item to Cart. One Cart Entry represents one item with multiple quantities by one user'''
  
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  item = models.ForeignKey(Item, related_name='cart', on_delete=models.CASCADE)
  user = models.ForeignKey(ExtendUser, related_name='cart', on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(null=False, blank=False)
  
  class Meta:
     constraints = [
            models.UniqueConstraint(fields=['item', 'user'], name='unique_item_user')
        ]

  def __str__(self):
    return f"{self.item} : {self.quantity}"