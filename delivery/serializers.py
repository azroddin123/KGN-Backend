from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import * 


class  DeliveryManSerializer(ModelSerializer):
    class Meta :
        model  = DeliveryMan
        fields = "__all__"
        
