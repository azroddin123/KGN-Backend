from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from django.db import transaction
from orders.serializers import * 
from orders.models import * 
from portals.GM2 import GenericMethodsMixin
from portals.services import paginate_data

class CartAPI(GenericMethodsMixin,APIView):
    model            = Cart
    serializer_class = CartSerializer
    lookup_field     = "id"
    
    def get(self,request,pk=None,*args,**kwargs):
        try : 
            if pk in [0,None] :
                data = Cart.objects.filter(user=request.thisUser.id)
                response = paginate_data(Cart,CartWithProductsSerializer,request,data)
                return Response(response,status=status.HTTP_200_OK)
            else :
                data = Cart.objects.filter(id=pk,user=request.thisUser.id)
                serializer = CartWithProductsSerializer(data)
                print(serializer.data,"--------------")
                return Response({"error" : False ,"data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

class CartItemAPI(GenericMethodsMixin,APIView):
    model            = CartItem
    serializer_class = CartItemSerializer
    lookup_field     = "id"
    
    def get(self,request,pk=None,*args,**kwargs):
        try : 
            if pk in [0,None] :
                data = CartItem.objects.filter(cart__user=request.thisUser.id)
                response = paginate_data(CartItem,CartItemSerializer1,request,data)
                return Response(response,status=status.HTTP_200_OK)
            else :
                data = CartItem.objects.filter(id=pk,cart__user=request.thisUser.id)
                serializer = CartItemSerializer(data)
                return Response({"error" : False ,"data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        
    def post(self,request,*args,**kwargs):
        try : 
            
            cart = Cart.objects.get(user=request.thisUser.id)
            request.POST._mutable = True
            print(cart,"------------------")
            request.data['cart'] = cart.id
            serializer = CartItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data" : serializer.data},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
    
class OrdersAPI(GenericMethodsMixin,APIView):
    model            = Orders
    serializer_class = OrdersSerializer
    lookup_field     = "id"
    

    
    
class OrderedItemAPI(GenericMethodsMixin,APIView):
    model            = OrderedItems
    serializer_class = OrderedItemSerializer1
    lookup_field     = "id"


class AddItemToCartAPI(APIView):
    def post(self,request,*args,**kwargs):
        try : 
            cart = Cart.objects.get(user=request.thisUser.id)
            request.POST._mutable = True
            request.data['cart'] = cart.id
            serializer = CartItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data" : serializer.data},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
        
class CustomerCartItemAPI(GenericMethodsMixin,APIView):
    model            = CartItem
    serializer_class = CartItemSerializer
    lookup_field     = "id"
   
    def get(self,request,pk=None,*args,**kwargs):
        try : 
            if pk in [0,None] :
                data = CartItem.objects.filter(cart__user=request.thisUser.id)
                response = paginate_data(CartItem,CartItemSerializer1,request,data)
                return Response(response,status=status.HTTP_200_OK)
            else :
                data = CartItem.objects.filter(id=pk,cart__user=request.thisUser.id)
                serializer = CartItemSerializer(data)
                return Response({"error" : False ,"data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    def post(self,request,*args,**kwargs):
        try : 
            cart = Cart.objects.get(user=request.thisUser.id)
            request.POST._mutable = True
            print(cart,"------------------")
            request.data['cart'] = cart.id
            serializer = CartItemSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.save()
                serializer_data = CartItemSerializer1(data)
                return Response({"data" : serializer_data.data},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)


class PlaceOrderAPI(APIView):
    def post(self,request,*args,**kwargs):
        try : 
            with transaction.atomic() : 
                cart = Cart.objects.get(user=request.thisUser.id)
                print(request)
                store_pincodes = StorePincode.objects.filter(pincode=request.thisUser.store_pincode).prefetch_related('store')
                request.POST._mutable = True
                request.data['store_id'] = store_pincodes.first().store.id
                request.data['user']  = request.thisUser.id
                request.data['cart']  = cart
                serializer     = OrdersSerializer(data=request.data)
                if serializer.is_valid():
                    order = serializer.save()
                    for cart in cart.cart_items.all() :
                        OrderedItems.objects.create(
                            order = order,
                            product = cart.product,
                            quantity = cart.quantity
                        )
                        product_obj = Inventory.objects.filter(store=store_pincodes.first().store.id,product=cart.product)
                        product_obj.update(stock=F('stock') - cart.quantity)
                    return Response({"data" : serializer.data},status=status.HTTP_200_OK)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

from rest_framework.exceptions import ValidationError


class PlaceOrderAPI1(APIView):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                
                # Fetch cart for the user
                cart = Cart.objects.prefetch_related('cart_items__product').get(user=request.thisUser.id)

                # Check if the cart has any items
                if not cart.cart_items.exists():
                    return Response({"error": True, "message": "Please Add Product in the cart First"}, status=status.HTTP_400_BAD_REQUEST)

                # Fetch store based on user's pincode
                store_pincode = StorePincode.objects.prefetch_related('store').filter(pincode=request.thisUser.store_pincode).first()

                # If no store matches the pincode
                if not store_pincode:
                    return Response({"error": True, "message": "No store available for the given pincode."}, status=status.HTTP_400_BAD_REQUEST)

                # Prepare data for order creation
                request.POST._mutable = True
                request.data.update({
                    'store_id': store_pincode.store.id,
                    'user': request.thisUser.id,
                    'cart': cart.id
                })

                # Serialize order data
                serializer = OrdersSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                order = serializer.save()

                # Iterate over cart items and create OrderedItems
                ordered_items = [
                    OrderedItems(
                        order=order,
                        product=item.product,
                        quantity=item.quantity
                    )
                    for item in cart.cart_items.all()
                ]
                OrderedItems.objects.bulk_create(ordered_items)

                # Update inventory in bulk for the store
                inventory_updates = []
                for item in cart.cart_items.all():
                    inventory_updates.append(
                        Inventory.objects.filter(store=store_pincode.store, product=item.product).update(
                            stock=F('stock') - item.quantity
                        )
                    )
                # Clear cart items once the order is placed
                cart.cart_items.all().delete()
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return Response({"error": True, "message": "Cart not found for this user."}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as ve:
            return Response({"error": True, "message": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ClearCartAPI(APIView):
     def get(self,request,pk=None,*args,**kwargs):
            # Fetch cart for the user
            cart = Cart.objects.prefetch_related('cart_items__product').get(user=request.thisUser.id)
              # Check if the cart has any items
            if not cart.cart_items.exists():
                return Response({"error": True, "message": "Please Add Product in the cart First"}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from django.shortcuts import get_object_or_404

class DeleteCartItemsView(APIView):
    def delete(self, request, *args, **kwargs):
        user = request.user
        
        # Get the user's cart
        cart = get_object_or_404(Cart, user=user)
        
        # Delete all CartItems related to the user's cart
        CartItem.objects.filter(cart=cart).delete()
        
        return Response({"message": "All cart items deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.env import Env
from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest
import uuid


TEST_MERCHANT_ID = "PGTESTPAYUAT100"
TEST_SALT_KEY    = "cc2f75ad-01c2-4417-92f8-32964ce8d12d"   
TEST_SALT_INDEX  = 1 
REDIRECT_URL     ="http://139.59.2.27:4000"
TEST_ENV         = "Env.UAT"


class OrderPaymentAPI(APIView):
     def post(self, request, *args, **kwargs):
        with transaction.atomic():
            try:
                # Fetch cart for the user
                cart = Cart.objects.prefetch_related('cart_items__product').get(user=request.thisUser.id)

                # Check if the cart has any items
                if not cart.cart_items.exists():
                    return Response({"error": True, "message": "Please Add Product in the cart First"}, status=status.HTTP_400_BAD_REQUEST)
                print("-----------",request.thisUser)
                # Fetch store based on user's pincode
                store_pincode = StorePincode.objects.prefetch_related('store').filter(pincode=request.thisUser.store_pincode).first()

                print(store_pincode,"-----------------")
                # If no store matches the pincode
                if not store_pincode:
                    return Response({"error": True, "message": "No store available for the given pincode."}, status=status.HTTP_400_BAD_REQUEST)

                # Prepare data for order creation
                request.POST._mutable = True
                request.data.update({
                    'store_id': store_pincode.store.id,
                    'user': request.thisUser.id,
                    'cart': cart.id
                })
                
                
                payment_type = request.data.get('payment_type')
                
                
                if payment_type == "UPI" :
                    merchant_id = TEST_MERCHANT_ID
                    salt_key = TEST_SALT_KEY  
                    salt_index = TEST_SALT_INDEX
                    env = TEST_ENV
                    phonepe_client = PhonePePaymentClient(
                        merchant_id=merchant_id,
                        salt_key=salt_key,
                        salt_index=salt_index,
                        env=env
                    )
                    # Generate unique transaction ID and URLs
                    unique_transaction_id = str(uuid.uuid4())[:-2]
                    print(unique_transaction_id)
                    ui_redirect_url =REDIRECT_URL
                    s2s_callback_url = REDIRECT_URL

                    # Validate and convert amount
                    amount = int(request.data.get('amount', 0)) * 100
                    if amount <= 0:
                        return Response({'error': True, 'message': "amount should be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)
                    request.POST._mutable = True
                    serializer = OrdersSerializer(data=request.data)
                    if serializer.is_valid():
                        order = serializer.save()
                        
                        
                           # Iterate over cart items and create OrderedItems
                        ordered_items = [
                            OrderedItems(
                                order=order,
                                product=item.product,
                                quantity=item.quantity
                            )
                            for item in cart.cart_items.all()
                        ]
                        OrderedItems.objects.bulk_create(ordered_items)

                        # Update inventory in bulk for the store
                        inventory_updates = []
                        for item in cart.cart_items.all():
                            inventory_updates.append(
                                Inventory.objects.filter(store=store_pincode.store, product=item.product).update(
                                    stock=F('stock') - item.quantity
                                )
                            )
                        # Clear cart items once the order is placed
                        cart.cart_items.all().delete()
                        
                        # Create PgPayRequest
                        id_assigned_to_user_by_merchant = TEST_MERCHANT_ID
                        pay_page_request = PgPayRequest.pay_page_pay_request_builder(
                            merchant_transaction_id=unique_transaction_id,
                            amount=amount,
                            merchant_user_id=id_assigned_to_user_by_merchant,
                            callback_url=REDIRECT_URL,
                            redirect_url=REDIRECT_URL,
                        )

                        # Send payment request and get the response URL
                        pay_page_response = phonepe_client.pay(pay_page_request)
                        pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
                        # Start payment status checking timer
                        # threading.Timer(360, check_payment_status, args=[unique_transaction_id]).start()
                        return Response({
                            "error": False,
                            "data": serializer.data,
                            'pay_page_url': pay_page_url,
                            "transaction_id": unique_transaction_id
                        }, status=status.HTTP_201_CREATED)
                    else:
                        # Collect and return serializer errors
                        error_list = [serializer.errors[error][0] for error in serializer.errors]
                        return Response({"error": True, "message": error_list}, status=status.HTTP_400_BAD_REQUEST)
            
                else :
                    unique_transaction_id = str(uuid.uuid4())[:-2]
                    print("unique transaction id -------> ",unique_transaction_id)
                    serializer = OrdersSerializer(data=request.data)
                    if serializer.is_valid():
                        order = serializer.save()
                        ordered_items = [
                            OrderedItems(
                                order=order,
                                product=item.product,
                                quantity=item.quantity
                            )
                            for item in cart.cart_items.all()
                        ]
                        OrderedItems.objects.bulk_create(ordered_items)

                        # Update inventory in bulk for the store
                        inventory_updates = []
                        for item in cart.cart_items.all():
                            inventory_updates.append(
                                Inventory.objects.filter(store=store_pincode.store, product=item.product).update(
                                    stock=F('stock') - item.quantity
                                )
                            )
                        # Clear cart items once the order is placed
                        cart.cart_items.all().delete()
                        return Response({
                            "error": False,
                            "data": serializer.data,
                            "transaction_id": unique_transaction_id
                        }, status=status.HTTP_201_CREATED)
                    else:
                        # Collect and return serializer errors
                        error_list = [serializer.errors[error][0] for error in serializer.errors]
                        return Response({"error": True, "message": error_list}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError as e:
                return Response({'error': True, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': True, 'message': 'An unexpected error occurred: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

 
class CustomerOrdersAPI(GenericMethodsMixin,APIView):
    model = Orders
    serializer_class = OrdersSerializer
    lookup_field ="id"  
    
    def get(self,request,pk=None,*args,**kwargs):
        # try : 
            if pk in ["0", None]:
               data = Orders.objects.filter(user=request.thisUser.id)
               print("len-data",data)
               response = paginate_data(Orders, OrderWithOrderedItemSerializer, request,data)
               return Response(response,status=status.HTTP_200_OK)
            else : 
               data = Orders.objects.get(id=pk,user=request.thisUser.id)
               serializer = OrderWithOrderedItemSerializer(data)
               return Response({"error" : False,"data" : serializer.data},status=status.HTTP_200_OK)
        # # except Exception as e:
        #     return Response({"error" : True , "message" : str(e) , "status_code" : 400},status=status.HTTP_400_BAD_REQUEST,)
    