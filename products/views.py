from django.shortcuts import render

# Create your views here.
from products.models import * 
from products.serializers import * 
from portals.GM2 import GenericMethodsMixin


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CategoryAPI(GenericMethodsMixin,APIView):
    model            = Category
    serializer_class = CategorySerializer
    lookup_field     = "id"

class SubCategoryAPI(GenericMethodsMixin,APIView):
    model            = SubCategory
    serializer_class = SubCategorySerializer
    lookup_field     = "id" 
    
class ProductAPI(GenericMethodsMixin,APIView):
    model            = Products
    serializer_class = ProductSerializer
    lookup_field     = "id"

