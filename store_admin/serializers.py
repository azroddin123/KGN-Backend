from rest_framework import serializers
from products.models import * 




class InventorySerializer1(serializers.ModelSerializer):
    product_name       = serializers.SerializerMethodField(read_only=True)
    store_name         = serializers.SerializerMethodField(read_only=True)
    product_image      = serializers.SerializerMethodField(read_only=True)
    
    class Meta :
        model  = Inventory
        fields = ('id','product','store','stock','last_updated','product_name','store_name','product_image')
    
    def get_product_name(self,obj):
        if obj.product :
            return obj.product.product_name
        return None
    
    def get_store_name(self,obj):
        if obj.store :
            return obj.store.store_name
        return None
    
    def get_product_image(self, obj):
        if obj.product and obj.product.product_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.product.product_image.url)
            return obj.product.product_image.url
        return None
        
            
        
    