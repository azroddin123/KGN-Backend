from django.shortcuts import render

# Create your views here.
from portals.services import paginate_data
from portals.GM2 import GenericMethodsMixin

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import * 
from products.serializers import * 

from orders.models import * 
from orders.serializers import * 


from .serializers import *
from django.db import transaction
import json



class StoreProductAPI(GenericMethodsMixin,APIView):
    model            = Product
    serializer_class = ProductSerializer
    lookup_field     = "id"
    
    def get(self,request,pk=None,*args,**kwargs):
        # try : 
           if pk in ["0", None]:
               data = Product.objects.all()
               response = paginate_data(Product, ProductSerializer, request,data)
               return Response(response,status=status.HTTP_200_OK)
           else : 
               data = Product.objects.get(id=pk)
               serializer = ProductSerializer(data)
               return Response({"error" : False,"data" : serializer.data},status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response({"error" : True , "message" : str(e) , "status_code" : 400},status=status.HTTP_400_BAD_REQUEST,)
    

class StoreAPI(GenericMethodsMixin,APIView):
    model = Store
    serializer_class = StoreSerializer
    lookup_field = "id"
    
    
    def get(self,request,pk=None,*args,**kwargs):
        try : 
           if pk in ["0", None]:
               data = Store.objects.filter(store_admin=request.thisUser.id)
               response = paginate_data(Store, StorePinSerializer, request,data)
               return Response(response,status=status.HTTP_200_OK)
           else : 
               data = Store.objects.get(id=pk)
               serializer = StorePinSerializer(data)
               return Response({"error" : False,"data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : True , "message" : str(e) , "status_code" : 400},status=status.HTTP_400_BAD_REQUEST,)
    
    def post(self,request,*args,**kwargs):
        with transaction.atomic():
            try : 
                pincode_list = request.data.get('pincode_list', '[]')
                pincode_list = json.loads(pincode_list)
                print("uploaded_pins",pincode_list)
                request.POST._mutable = True
                request.data['store_admin'] = request.thisUser.id
                serializer = StoreSerializer(data=request.data)
                if serializer.is_valid():
                    store = serializer.save()
                    pin_list = [StorePincode(pincode=pin,store=store) for pin in pincode_list]
                    StorePincode.objects.bulk_create(pin_list)
                    serializer = StorePinSerializer(store)
                    return Response({"error" : False, "data" : serializer.data},status=status.HTTP_201_CREATED)
                return Response({"error" : True , "errors" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e :
                return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)
            
    def put(self,request,pk=None,*args,**kwargs):
        with transaction.atomic():
            try : 
                
                store_object = Store.objects.get(id=pk)
                
                pincode_list = request.data.get('pincode_list', '[]')
                pincode_list = json.loads(pincode_list)
                print("uploaded_pins",pincode_list)
                request.POST._mutable = True
                serializer = StoreSerializer(store_object,data=request.data,partial=True)
                if serializer.is_valid():
                    store = serializer.save()
                    if pincode_list : 
                        data = StorePincode.objects.filter(store=store)
                        data.delete()
                        pin_list = [StorePincode(pincode=pin,store=store) for pin in pincode_list]
                        StorePincode.objects.bulk_create(pin_list)
                    serializer = StorePinSerializer(store)
                    return Response({"error" : False, "data" : serializer.data},status=status.HTTP_201_CREATED)
                return Response({"error" : True , "errors" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e :
                return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)


class StoreInventoryAPI(GenericMethodsMixin,APIView):
    model = Inventory
    serializer_class = InventorySerializer
    lookup_field ="id"    

    def get(self,request,pk=None,*args,**kwargs):
        try : 
           if pk in ["0", None]:
               data = Inventory.objects.filter(store__store_admin=request.thisUser.id).order_by('-created_on')
               response = paginate_data(Inventory, InventorySerializer1, request,data)
               return Response(response,status=status.HTTP_200_OK)
           else : 
               data = Inventory.objects.get(id=pk)
               serializer = InventorySerializer1(data)
               return Response({"error" : False,"data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : True , "message" : str(e) , "status_code" : 400},status=status.HTTP_400_BAD_REQUEST,)
    
    
    
class StoreOrdersAPI(GenericMethodsMixin,APIView):
    model = Orders
    serializer_class = OrdersSerializer
    lookup_field ="id"  
    
    
    def get(self,request,pk=None,*args,**kwargs):
        # try : 
           if pk in ["0", None]:
               data = Orders.objects.filter(store_id__store_admin=request.thisUser.id)
               print("len-data---------",data)
               response = paginate_data(Orders, OrderWithOrderedItemSerializer, request,data)
               return Response(response,status=status.HTTP_200_OK)
           else : 
               data = Orders.objects.get(id=pk)
               serializer = OrderWithOrderedItemSerializer(data)
               return Response({"error" : False,"data" : serializer.data},status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response({"error" : True , "message" : str(e) , "status_code" : 400},status=status.HTTP_400_BAD_REQUEST,)



# class AssignOrderAPI(APIView):
#     def put(self,request,*args,**kwargs):
        
#         pass
    