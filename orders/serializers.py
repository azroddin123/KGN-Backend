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
    product_name   = serializers.SerializerMethodField(read_only=True)
    product_image  = serializers.SerializerMethodField(read_only=True)
    product_price  = serializers.SerializerMethodField(read_only=True)
    
    class Meta :
        model = CartItem
        fields = ('id','product','product_name','product_image','quantity','product_price')
        
    def get_product_name(self,obj):
        if obj.product :
            return obj.product.product_name
        return None
    
    def get_product_price(self,obj):
        if obj.product :
            return obj.product.price
        return None
    
    def get_product_image(self, obj):
        if obj.product and obj.product.product_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.product.product_image.url)
            return obj.product.product_image.url
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
    cart_items = CartItemSerializer1(many=True,read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model = Cart
        fields = ('id','user','total_price','cart_items')
        
    def get_user(self,obj):
        if obj.user:
            return obj.user.username
        return None