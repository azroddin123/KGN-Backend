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


class CartItemSerializer1(ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model = CartItem
        fields = ('id','product','quantity',)
        
    def get_product(self,obj):
        if obj.product :
            return obj.product.product_name
        return None
        

class OrdersSerializer(ModelSerializer):
    class Meta : 
        model = Orders
        fields = "__all__"
        

class OrderedItemSerializer(ModelSerializer):
    class Meta :
        model = OrderedItems
        fields = "__all__"
        
        

class CartWithProductsSerializer(ModelSerializer):
    cart = CartItemSerializer1(many=True,read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model = Cart
        fields = ('id','user','total_price','cart')
        
    def get_user(self,obj):
        if obj.user:
            return obj.user.username
        return None