from rest_framework.serializers import ModelSerializer
from products.models import *



class CategorySerializer(ModelSerializer):
    class Meta :
        model = Category
        fields = "__all__"
        

class SubCategorySerializer(ModelSerializer):
    class Meta :
        model = SubCategory
        fields = "__all__"
        

class ProductSerializer(ModelSerializer):
    class Meta :
        model = Products
        fields = "__all__"
        
        