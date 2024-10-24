from django.db import models
from portals.models import BaseModel
# Create your models here.

class Category(BaseModel):
    category_name  = models.CharField(max_length=128)
    category_image = models.ImageField(upload_to="category",null=True,blank=True)
    category_description = models.TextField(null=True,blank=True)


class SubCategory(BaseModel):
    name                  = models.CharField(max_length=258)
    category              = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    description           = models.TextField(null=True,blank=True)

class Products(BaseModel):
    name         = models.CharField(max_length=128)
    category     = models.ForeignKey(SubCategory,on_delete=models.CASCADE,null=True,blank=True)
    price        = models.PositiveIntegerField()
    stock        = models.PositiveIntegerField()
    description  = models.TextField(null=True,blank=True)