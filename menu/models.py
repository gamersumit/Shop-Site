import uuid
from django.db import models
import uuid
# Create your models here.

class Category(models.Model):
  ''' 
  Category Model to defined different tyes of item/ to categorise items
  e.g. -> Breakfast, Dinner, Lunch, Shakes, Chinese etc...
  'name' is the only field and is primary key
  '''
  name = models.CharField(max_length=50, primary_key = True, blank=False, null=False)
  
  def __str__(self):
      return self.name
      
class Item(models.Model):
  ''' Product/Item Model to query data releated to Product/Item 
  of the resturant maintained by Restuarant Owner/Admin '''
  
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(unique=True, max_length=255, verbose_name = 'ITEM NAME', blank=False, null=False)
  price = models.PositiveIntegerField(verbose_name='ITEM PRICE')
  category = models.ManyToManyField(Category, related_name = 'item', blank=True)
  is_deleted = models.BooleanField(default=False, verbose_name='SOFT DELETE ITEM')
  
  def __str__(self):
    return self.name