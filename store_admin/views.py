from django.shortcuts import render

# Create your views here.
from portals.services import paginate_data
from portals.GM2 import GenericMethodsMixin

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import * 
from products.serializers import * 
from .serializers import *

class StoreProductAPI(GenericMethodsMixin,APIView):
    model            = Product
    serializer_class = ProductSerializer
    lookup_field     = "id"
    
    def get(self,request,pk=None,*args,**kwargs):
        # try : 
           if pk in ["0", None]:
               data = Product.objects.all()
               response = paginate_data(Product, ProductSerializer, request,data)
               return Response(response,status=status.HTTP_200_OK)
           else : 
               data = Product.objects.get(id=pk)
               serializer = ProductSerializer(data)
               return Response({"error" : False,"data" : serializer.data},status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response({"error" : True , "message" : str(e) , "status_code" : 400},status=status.HTTP_400_BAD_REQUEST,)
    

class StoreAPI(GenericMethodsMixin,APIView):
    model = Store
    serializer_class = StoreSerializer
    lookup_field = "id"
    
    
    def get(self,request,pk=None,*args,**kwargs):
        try : 
           if pk in ["0", None]:
               data = Store.objects.filter(store_admin=request.thisUser.id)
               response = paginate_data(Store, StoreSerializer, request,data)
               return Response(response,status=status.HTTP_200_OK)
           else : 
               data = Store.objects.get(id=pk)
               serializer = StoreSerializer(data)
               return Response({"error" : False,"data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : True , "message" : str(e) , "status_code" : 400},status=status.HTTP_400_BAD_REQUEST,)
    
    
class StoreInventoryAPI(GenericMethodsMixin,APIView):
    model = Inventory
    serializer_class = InventorySerializer
    lookup_field ="id"    
    
    def get(self,request,pk=None,*args,**kwargs):
        try : 
           if pk in ["0", None]:
               data = Inventory.objects.filter(store__store_admin=request.thisUser.id)
               response = paginate_data(Inventory, InventorySerializer1, request,data)
               return Response(response,status=status.HTTP_200_OK)
           else : 
               data = Inventory.objects.get(id=pk)
               serializer = InventorySerializer1(data)
               return Response({"error" : False,"data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : True , "message" : str(e) , "status_code" : 400},status=status.HTTP_400_BAD_REQUEST,)
    
    
    
