from turtle import update
from unicodedata import category
import graphene
from graphene_django import DjangoObjectType
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

    

class Query(graphene.ObjectType):
    category = graphene.Field(CategoryType, name = graphene.String())
    categories = graphene.List(CategoryType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    def resolve_category(self, info, name):
        try:
          return Category.objects.get(name = name)
        except :
          return 
    
    def resolve_categories(self, info):
        return Category.objects.all()


class CreateCategory(graphene.Mutation):
  class Arguments:
    name = graphene.String(required = True)
  
  category = graphene.Field(CategoryType)
  
  @classmethod
  def mutate(cls, root, info, name):
    # create
    category = Category(name=name)
    category.save()
    return CreateCategory(category=category)
  
class UpdateCategory(graphene.Mutation):
  class Arguments:
    id = graphene.Int(required=True)
    name = graphene.String(required = True)
  
  category = graphene.Field(CategoryType)
  
  @classmethod
  def mutate(cls, root, info, id, name):
    # create
    try : 
      category = Category.objects.get(pk=id)
      category.name = name
      category.save()
      return UpdateCategory(category=category)
    except Exception as e:
      raise Exception('Does not exsits')

class DeleteCategory(graphene.Mutation):
  class Arguments:
    id = graphene.Int(required=True)
  
  
  errors = graphene.List(graphene.String)
  success = graphene.Boolean()
  category = graphene.Field(CategoryType)
  status_code = graphene.Int()
  
  @permissions_checker([IsAuthenticated])
  def mutate(cls, info, id):
    try :
      print(info.context.user)
      print(info.context.session.session_key)
      category = Category.objects.get(pk=id)
      category.delete()
      return DeleteCategory(success=False, errors=None, status_code = 200)
    
    except Exception as e:
      return DeleteCategory(success=False, errors = [str(e)], status_code = 404)

class Mutation(graphene.ObjectType):
  create_category = CreateCategory.Field()
  update_category = UpdateCategory.Field()
  delete_category = DeleteCategory.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)