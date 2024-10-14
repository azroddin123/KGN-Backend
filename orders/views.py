from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
                serializer.save()
                return Response({"data" : serializer.data},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
            
        


class PlaceOrderAPI(APIView):
        
    def post(self,request,*args,**kwargs):
        try : 
            with transaction.atomic() : 
                cart = Cart.objects.get(user=request.thisUser.id)
                request.POST._mutable = True
                
                serializer = OrdersSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"data" : serializer.data},status=status.HTTP_200_OK)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)