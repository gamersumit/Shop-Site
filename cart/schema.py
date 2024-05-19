from unicodedata import category
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
    cart = graphene.List(CartType)
    
    def resolve_cart(self, info):
      if not info.context.user.is_authenticated:
          raise GraphQLError("You must be authenticated to access this resource.")
      return Cart.objects.filter(user = info.context.user)


class AddToCart(graphene.Mutation):
    ''' Mutation For updation/deletion/addition of items in the cart. It takes two arguments:
    1. item(id) to add item in the cart
    2. quantity(int) to specify no of units for that item to add.
    To differentiate Cart for multiple users this api/action is only for authenticated user.

     # if qantity argument is '0'  and the item is alreday present in the user's cart it will be removed from the cart if not present the nothing in the cart will be changed.
     # if item is already present in the user's then it will be updated with qantity argument.
     # if item not present in the user's cart it will be added.
    '''
    class Arguments:
      item = graphene.ID(required = True)
      quantity = graphene.Int(required = True)
    

    cart = graphene.List(CartType)
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, **kwargs):
      try : 
        user = info.context.user
        cart = Cart.objects.filter(user = user)
        item = Item.objects.get(id = kwargs['item'])
        quantity = kwargs['quantity']
        cart_item = cart.filter(item = item).first()
        cart = list(cart)
        
        if cart_item :
          cart.remove(cart_item)
          if quantity == 0:
            cart_item.delete()
            return AddToCart(success = True, errors = None, cart = cart)

          cart_item.quantity = quantity

        elif quantity == 0:
          return AddToCart(success = True, errors = None, cart = cart)

        cart_item = Cart(item = item, user = user, quantity=quantity)
        cart_item.save()
        cart.append(cart_item)
        return AddToCart(success=True, errors=None, cart = cart)
      
      except Exception as e:
        return AddToCart(success=False, errors=[str(e)], cart = cart)




class CartMutation(graphene.ObjectType):
  add_to_cart = AddToCart.Field()


