from django.shortcuts import render

# Create your views here.
from products.models import * 
from products.serializers import * 
from portals.GM2 import GenericMethodsMixin
from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class StoreAPI(GenericMethodsMixin,APIView):
    model            = Store
    serializer_class = StoreSerializer
    lookup_field     = "id"
    
class CategoryAPI(GenericMethodsMixin,APIView):
    model            = Category
    serializer_class = CategorySerializer
    lookup_field     = "id"

class SubCategoryAPI(GenericMethodsMixin,APIView):
    model                   = SubCategory
    serializer_class        = SubCategorySerializer
    create_serializer_class = SubCategorySerializer1
    lookup_field            = "id" 
    
class ProductAPI(GenericMethodsMixin,APIView):
    model            = Product
    serializer_class = ProductSerializer
    lookup_field     = "id"

class InventoryAPI(GenericMethodsMixin,APIView):
    model            = Inventory
    serializer_class = InventorySerializer
    lookup_field     = "id"
  
  
import json  
class AddStoreAPI(GenericMethodsMixin,APIView):
    model = Store
    serializer_class = StorePinSerializer
    lookup_field = "id"
    
    def post(self,request,*args,**kwargs):
        with transaction.atomic():
            try : 
                pincode_list = request.data.get('pincode_list', '[]')
                pincode_list = json.loads(pincode_list)
                print("uploaded_pins",pincode_list)
                request.POST._mutable = True
                request.data['store_admin'] = request.thisUser.id
                serializer = StoreSerializer(data=request.data)
                if serializer.is_valid():
                    store = serializer.save()
                    pin_list = [StorePincode(pincode=pin,store=store) for pin in pincode_list]
                    StorePincode.objects.bulk_create(pin_list)
                    serializer = StorePinSerializer(store)
                    return Response({"error" : False, "data" : serializer.data},status=status.HTTP_201_CREATED)
                return Response({"error" : True , "errors" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e :
                return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

