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
        
class CategorySubCategorySerializer(ModelSerializer):
    subcategory = SubCategorySerializer1(many=True,read_only=True)
    class Meta :
        model = Category
        fields = ('id','category_name','category_description','category_image','subcategory')
        


class ProductSerializer(ModelSerializer):
    sub_category_name = serializers.SerializerMethodField()
    class Meta :
        model = Product
        exclude = ("created_on","updated_on")
    
    def get_sub_category_name(self,obj):
        if obj.sub_category:
            return obj.sub_category.name
        return None


class ProductSubCategorySerializer(ModelSerializer):
    products = ProductSerializer(many=True,read_only=True)
    class Meta :
            model = SubCategory
            fields = ('id','name','category','description','category_image','products')
            
            
class InventorySerializer(ModelSerializer):
    class Meta :
        model = Inventory
        fields = ("__all__")
        

class StoreSerializer(ModelSerializer):
    class Meta :
        model = Store
        exclude = ("created_on","updated_on")

class SPSerializer(ModelSerializer):
    class Meta :
        model = StorePincode
        fields=('pincode',)

class StorePinSerializer(ModelSerializer):
    store_admin = serializers.SerializerMethodField()
    pincodes = SPSerializer(many=True,read_only=True)
    class Meta :
        model = Store 
        fields = ('id','store_name','store_address','store_admin','store_image','pincodes')
    
    def get_store_admin(self,obj):
        if obj.store_admin:
            return obj.store_admin.username
        return None
        