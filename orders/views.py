from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction
from orders.serializers import * 
from orders.models import * 
from portals.GM2 import GenericMethodsMixin

class CartAPI(GenericMethodsMixin,APIView):
    model            = Cart
    serializer_class = CartSerializer
    lookup_field     = "id"

class CartItemAPI(GenericMethodsMixin,APIView):
    model            = CartItem
    serializer_class = CartItemSerializer
    lookup_field     = "id"
    
class OrdersAPI(GenericMethodsMixin,APIView):
    model            = Orders
    serializer_class = OrdersSerializer
    lookup_field     = "id"
    
class OrderedItemAPI(GenericMethodsMixin,APIView):
    model            = OrderedItems
    serializer_class = OrderedItemSerializer
    lookup_field     = "id"
    