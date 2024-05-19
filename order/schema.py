from unicodedata import category
import graphene
from django.db import transaction
from graphene_django import DjangoObjectType
from graphene_django_cud import mutations
from cart.models import Cart
from menu.models import Item
from graphql import GraphQLError
from django_graphene_permissions.permissions import IsAuthenticated
from django_graphene_permissions import permissions_checker
from django.contrib.auth.decorators import login_required
from permissions import AdminPermission
from .models import OrderItems, Order
from decimal import Decimal

# queryies 

class OrderItemsType(DjangoObjectType):
    ''' Definig Structure for Order Items '''
    class Meta:
        model = OrderItems
        fields = ("id", "item", "price", "quantity")

class OrderDetailsType(DjangoObjectType):
  '''
  Specifying Fields that can be viewed by frontend for Order Details
  '''

  class Meta:
      model = Order
      fields = ("id", "ordered_at", "subtotal_amount", "tax_rate", "tax_amount", "discount_rate", "discount_amount", "total_amount", "order_items")

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
      
      return Order.objects.filter(user = info.context.user)


    def resolve_order_details(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError("You must be authenticated to access this resource.")
        
        return Order.objects.filter(user = info.context.user, id = id).first()
        
        # return Order.objects.filter(user = info.context.user, id = id).first()

class PlaceOrder(graphene.Mutation):
    '''
     API To Place Order which can be integrated with Payment later.
      >> For now authenticated user just need to make a place order request with no arguments.
      >> Here we will fetch CART for that User and calculate the sub total amount of the order.
      >> Then we will create Order object to get a order.id. Now pre_save() signal for model order will 
          fill all the remaining details like tax_rate, tax_amount, discount_rate, discount_amount, total_amount etc.
      >> Then will add cart items into order(orderItems model) referenced with the order id
      >> when everythings done we will empty the CART.
      >> Everything should be done under db transaction.
    '''




    order_details = graphene.Field(OrderDetailsType)
    errors = graphene.List(graphene.String)
    success = graphene.Boolean()

    # class Argument :
    #   # ask for bank account/upi detils, so we can make a payment request.abs
    #   # upi id 
    #   # phone number
    #   # cc
    #   # db
    #   # cash

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, **kwargs):
      try :
        user = info.context.user
        cart = Cart.objects.filter(user = user)
        
        # fetch payment/account details from **kwargs

        if not cart :
          return PlaceOrder(OrderDetailsType = None, success = False, errors = ['To Place a Order you must Choose at least one Item'])
       
        with transaction.atomic():
          item = cart.first()
          subtotal_amount = Decimal(1.0 * float(sum(item.item.price * item.quantity for item in cart))) 
          
          # we can call a payment api / for razor pay/ debit card etc and send a request to user's upi etc or it might be cash
          # pay_response = wait for the payment response

          # proceed when payment suceesfull
          order = Order(user = user, subtotal_amount = subtotal_amount)
          order.save()

          # save payment details to a payment table referenced with order.id
          # e.g :- payment = Payment(order = order, transaction_id = response['transaction_id'] or 'CASH, method = 'UPI' etc..)
          # payment.save()

          # continue :-   
          for item in cart :
            order_item = OrderItems(order = order, item = item.item, quantity = item.quantity, price = item.item.price * item.quantity)
            order_item.save()

          cart.delete()
          return PlaceOrder(success = True, errors = None, order_details = order)
      
      except Exception as e:
        return PlaceOrder(success=False, errors=[str(e)], order_details = None)

class OrderMutation(graphene.ObjectType):
  place_order = PlaceOrder.Field()


