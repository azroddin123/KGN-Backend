from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import * 


class CartSerializer(ModelSerializer):
    class Meta :
        model = Cart
        fields = "__all__"
        

class CartItemSerializer(ModelSerializer):
    class Meta :
        model = CartItem
        fields = "__all__"
        

class OrdersSerializer(ModelSerializer):
    class Meta : 
        model = Orders
        fields = "__all__"
        

class OrderedItemSerializer(ModelSerializer):
    class Meta :
        model = OrderedItems
        fields = "__all__"
        
        

class CartWithProductsSerializer(ModelSerializer):
    cart = CartItemSerializer(many=True,read_only=True)
    class Meta :
        model = Cart
        fields = ('id','user','total_price','cart')