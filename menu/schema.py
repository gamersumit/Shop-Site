from importlib.metadata import requires
from turtle import update
from unicodedata import category
import graphene
from graphene_django import DjangoObjectType
from graphene_django_cud.mutations import DjangoDeleteMutation
from .models import Category, Item
from django_graphene_permissions.permissions import IsAuthenticated
from django_graphene_permissions import permissions_checker
from user.permissions import AdminPermission

 
class ItemType(DjangoObjectType):
  '''
  To Query on Category Table 
  '''
  class Meta:
      model = Item
      fields = ("id", "name", "price", "category")

class CategoryType(DjangoObjectType):
  '''
  FLEXIBLE Query on Category Table with the list of items related items
  '''
  items = graphene.List(ItemType)
  class Meta:
      model = Category
      fields= ('name', 'items')
      
  def resolve_items(self, info):
      return self.item.filter(is_deleted = False)

class MenuQuery(graphene.ObjectType):
    category = graphene.Field(CategoryType, name = graphene.String())
    categories = graphene.List(CategoryType)
    items = graphene.List(ItemType)
    
    def resolve_category(self, info, name):
        try:
          return Category.objects.get(name = name)
        except :
          return Category.objects.none()
    
    def resolve_categories(self, info):
        return Category.objects.all()
    
    def resolve_items(self, info):
        return Item.objects.all()


class CreateCategory(graphene.Mutation):
  class Arguments:
    name = graphene.String(required = True)
  
  category = graphene.String()
  errors = graphene.List(graphene.String)
  success = graphene.Boolean()
  
  
  @permissions_checker([IsAuthenticated])
  def mutate(self, info, name):
    # create
    try: 
      if Category.objects.filter(name = name).exists() :
        raise Exception('Category Already Exists')
      category = Category(name=name)
      category.save()
      return CreateCategory(success=True, errors=None, category=name)
    
    except Exception as e:
      return CreateCategory(success=False, errors=[str(e)], category=None)
    
class UpdateCategory(graphene.Mutation):
  class Arguments:
    old_name = graphene.String(required = True)
    new_name = graphene.String(required = True)
  
  category = graphene.String()
  errors = graphene.List(graphene.String)
  success = graphene.Boolean()

  @permissions_checker([IsAuthenticated])
  def mutate(self, info, old_name, new_name):
    # update 
    try : 
      category = Category.objects.get(name=old_name)
      category.name = new_name
      category.save()
      return UpdateCategory(success=True, errors=None, category=new_name)
    
    except Exception as e:
      raise UpdateCategory(success=False, errors=[str(e)], category=None)

class DeleteCategory(DjangoDeleteMutation):
  class Meta:
        model = Category
        permissions = [IsAuthenticated]

class MenuMutation(graphene.ObjectType):
  create_category = CreateCategory.Field()
  update_category = UpdateCategory.Field()
  delete_category = DeleteCategory.Field()

