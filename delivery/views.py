from django.shortcuts import render

# Create your views here

from orders.models import * 
from orders.serializers import *

from .models import * 
from .serializers import * 

from random import randint
from django.db import transaction

# Create your views here.
from portals.services import paginate_data
from portals.GM2 import GenericMethodsMixin

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView



class DeliveryManAPI(GenericMethodsMixin,APIView):
    model            = DeliveryMan
    serializer_class = DeliveryManSerializer
    lookup_field     = "id"
    
    def post(self,request,*args,**kwargs):
        try : 
            user_id               = request.thisUser.id 
            request.POST._mutable = True
            request.data['user'] = user_id
            serializer = DeliveryManSerializer(data=request.data)
            if  serializer.is_valid():
                serializer.save()
                return Response({"error" : False,"message" : "Delivery Man Profile Created Successfully" , "data" :serializer.data},status=status.HTTP_201_CREATED)
            error_list = [serializer.errors[error][0] for error in serializer.errors]
            return Response({"error": True, "message": error_list}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error" : True , "message" : str(e) , "status_code" : 400},status=status.HTTP_400_BAD_REQUEST,)

    
    


  