from django.shortcuts import render

# Create your views here.
from products.models import * 
from products.serializers import * 
from portals.GM2 import GenericMethodsMixin


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