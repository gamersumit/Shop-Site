import graphene
from graphene_django import DjangoObjectType
from graphene_django_cud import mutations
from .models import Cart
from menu.models import Item
from graphql import GraphQLError
from django_graphene_permissions.permissions import IsAuthenticated
from django_graphene_permissions import permissions_checker
from django.contrib.auth.decorators import login_required
from permissions import AdminPermission

# queryies 
class CartType(DjangoObjectType):
  '''
  Fields structure To Query on Cart Table
  '''
  class Meta:
      model = Cart
      fields = ("id", "item", "quantity")


class CartQuery(graphene.ObjectType):
    cart_items = graphene.List(CartType)
    
    def resolve_cart_items(self, info):
      if not info.context.user.is_authenticated:
          raise GraphQLError("You must be authenticated to access this resource.")
      return Cart.objects.filter(user = info.context.user)





# # category --->
# class CreateCategory(graphene.Mutation):
#   class Arguments:
#     name = graphene.String(required = True)
  
#   category = graphene.String()
#   errors = graphene.List(graphene.String)
#   success = graphene.Boolean()
  
  
#   @permissions_checker([IsAuthenticated])
#   def mutate(self, info, name):
#     # create
#     try: 
#       if Category.objects.filter(name = name).exists() :
#         raise Exception('Category Already Exists')
#       category = Category(name=name)
#       category.save()
#       return CreateCategory(success=True, errors=None, category=name)
    
#     except Exception as e:
#       return CreateCategory(success=False, errors=[str(e)], category=None)
    
# class UpdateCategory(graphene.Mutation):
#   class Arguments:
#     old_name = graphene.String(required = True)
#     new_name = graphene.String(required = True)
  
#   category = graphene.String()
#   errors = graphene.List(graphene.String)
#   success = graphene.Boolean()

#   @permissions_checker([IsAuthenticated])
#   def mutate(self, info, old_name, new_name):
#     # update 
#     try : 
#       category = Category.objects.get(name=old_name)
#       category.name = new_name
#       category.save()
#       return UpdateCategory(success=True, errors=None, category=new_name)
    
#     except Exception as e:
#       raise UpdateCategory(success=False, errors=[str(e)], category=None)

# class DeleteCategory(graphene.Mutation):
#   class Arguments:
#        name = graphene.String(required = True)
  
#   found = graphene.Boolean()
#   deleted_key = graphene.String()
  
#   @permissions_checker([AdminPermission])
#   def mutate(self, info, name):
#     try : 
#       category = Category.objects.get(name=name)
#       category.delete()
#       return DeleteCategory(found = True, category=name)
    
#     except Exception as e:
#       raise DeleteCategory(found = False, category=None)



# # item --->
# class CreateItems(mutations.DjangoBatchCreateMutation):
#     class Meta:
#       model = Item
#       only_fields = ['name', 'category', 'price']
#       optional_fields = ('category',)
#       return_field_name = 'items'
#       permissions = [AdminPermission]

# class DeleteItems(mutations.DjangoBatchDeleteMutation):
#   class Meta:
#     model = Item
#     permissions = [AdminPermission]

# class UpdateItem(graphene.Mutation):
#     class Arguments:
#       id = graphene.ID(required = True)
#       name = graphene.String()
#       price = graphene.Int()
#       deleted_categories = graphene.List(graphene.String)
#       added_categories = graphene.List(graphene.String)
  
#     item = graphene.Field(ItemType)
#     errors = graphene.List(graphene.String)
#     success = graphene.Boolean()

#     @permissions_checker([IsAuthenticated])
#     def mutate(self, info, **kwargs):
#       # update 
#       try : 
#         id = kwargs['id']
#         name = kwargs.get('name')
#         price = kwargs.get('price')
#         deleted_categories = kwargs.get('deleted_categories', [])
#         added_categories = kwargs.get('added_categories', [])
#         item = Item.objects.get(id = id)
        
#         if name:
#           item.name = name
        
#         if price:
#           item.price = price
        
#         if len(deleted_categories) != 0 and item.category:
#           for category in deleted_categories:
#             try :
#               item.category.remove(category)
#             except :
#               continue
            
#         if len(added_categories) != 0:
#           if not item.category :
#             item.category = added_categories
          
#           else:
#             for category in added_categories:
#               try :
#                   item.category.add(category)    
#               except Exception as e:
#                 continue
            
#         item.save()
#         return UpdateItem(success=True, errors=None, item = item)
      
#       except Exception as e:
#         raise UpdateItem(success=False, errors=[str(e)], item = None)


# # menu
class CartMutation(graphene.ObjectType):
  pass
#   create_category = CreateCategory.Field()
#   update_category = UpdateCategory.Field()
#   delete_category = DeleteCategory.Field()
#   create_items = CreateItems.Field()
#   delete_items = DeleteItems.Field()
#   update_item = UpdateItem.Field()

