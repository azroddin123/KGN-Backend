from rest_framework import serializers
from products.models import * 




class InventorySerializer1(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)
    store   = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model  = Inventory
        fields = ('product','store','stock','last_updated')
    
    def get_product(self,obj):
        if obj.product :
            return obj.product.product_name
        return None
    
    def get_store(self,obj):
        if obj.store :
            return obj.store.store_name
        return None
        
            
        
    