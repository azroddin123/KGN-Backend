from django.db import models
from portals.models import BaseModel


class ServiceArea(BaseModel):
    area_name = models.CharField(max_length=256,null=True,blank=True)
    pin_code  = models.CharField(max_length=256,null=True,blank=True)
    
# Create your models here.
class Store(BaseModel):
    store_name     = models.CharField(max_length=256,null=True,blank=True)
    store_address  = models.CharField(max_length=256,null=True,blank=True)
    pincode        = models.CharField(max_length=6,null=True,blank=True)
