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
class OrderDetailsType(DjangoObjectType):
  '''
  Specifying Fields that can be viewed by frontend for Order Details
  '''

  class Meta:
      model = Payment
      fields = ("id", "total", "subtotal", "discount", "tax", "paid_at", "order_details")


class OrderQuery(graphene.ObjectType):
    ''' 
    1. Fetch Mutilple/all orders details for a user.
    2. Fetch a single order details with ORDER ID.
      # order(s) must belong to the user who is making request 
    '''
    
    orders_details = graphene.List(OrderDetailsType)
    order_details = graphene.Field(OrderDetailsType, id = graphene.ID())

    
    def resolve_orders_details(self, info):
      if not info.context.user.is_authenticated:
          raise GraphQLError("You must be authenticated to access this resource.")
      return Payment.objects.filter(user = info.context.user)


    def resolve_order_details(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be authenticated to access this resource.")

        return Payment.objects.filter(user = info.context.user, id = id)


class MakeOrder(graphene.Mutation):
    
    class Arguments:
      pass

    
    
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




class OrderMutation(graphene.ObjectType):
  make_order = MakeOrder.Field()


