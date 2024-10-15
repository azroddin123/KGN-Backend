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
    serializer_class = OrderedItemSerializer
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
