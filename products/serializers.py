from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from products.models import *



class CategorySerializer(ModelSerializer):
    class Meta :
        model = Category
        exclude = ("created_on","updated_on")

class SubCategorySerializer(ModelSerializer):
    main_category_name   = serializers.SerializerMethodField()
    class Meta :
        model = SubCategory
        fields = "__all__"
    def get_main_category_name(self,obj):
        if obj.category:
            return obj.category.category_name
        return None
    
class SubCategorySerializer1(ModelSerializer):
    class Meta :
        model = SubCategory
        exclude = ("created_on","updated_on")
        
class ProductSerializer(ModelSerializer):
    sub_category_name = serializers.SerializerMethodField()
    class Meta :
        model = Product
        exclude = ("created_on","updated_on")
    
    def get_sub_category_name(self,obj):
        if obj.sub_category:
            return obj.sub_category.name
        return None
    
class InventorySerializer(ModelSerializer):
    class Meta :
        model = Inventory
        fields = ("__all__")
        

class StoreSerializer(ModelSerializer):
    class Meta :
        model = Store
        exclude = ("created_on","updated_on")
        