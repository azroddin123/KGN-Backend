# Create your views here.
from products.models import * 
from products.serializers import * 
from portals.GM2 import GenericMethodsMixin
from portals.services import paginate_data

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
    model            = Product
    serializer_class = ProductSerializer
    lookup_field     = "id"
    

class StoreApi(GenericMethodsMixin,APIView):
    model = Store
    serializer_class = StoreSerializer
    lookup_field     = "id"
    
    
class GetSubcategoriesAPI(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        # try : 
           if pk in ["0", None]:
                category_id = request.GET.get('category_id')
                if category_id is None :
                    data = SubCategory.objects.all()
                else : 
                    data = SubCategory.objects.filter(category=category_id)
                response = paginate_data(SubCategory, SubCategorySerializer, request,data)
                return Response(response,status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response({"error" : True , "message" : str(e) , "status_code" : 400},status=status.HTTP_400_BAD_REQUEST,)


class GetAllProductsBySubCategoryAPI(GenericMethodsMixin,APIView):
    def get(self, request, pk=None, *args, **kwargs):
        try : 
               sub_category = request.GET.get('sub_category')
               if sub_category is None : 
                    data = Product.objects.all()
               else :
                    data = Product.objects.filter(sub_category=sub_category)
               response = paginate_data(Product, ProductSerializer, request,data)
               return Response(response,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : True , "message" : str(e) , "status_code" : 400},status=status.HTTP_400_BAD_REQUEST,)

