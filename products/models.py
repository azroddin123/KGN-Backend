from django.db import models
from portals.models import BaseModel
import os 


class Category(BaseModel):
    category_name        = models.CharField(max_length=128)
    category_image       = models.ImageField(upload_to="category/",null=True,blank=True)
    category_description = models.TextField(null=True,blank=True)
    
    
    def delete(self, *args, **kwargs):
        if self.category_image:
            if os.path.isfile(self.category_image.path):
                os.remove(self.category_image.path)
        super(Category, self).delete(*args, **kwargs)

class SubCategory(BaseModel):
    name                  = models.CharField(max_length=258)
    category              = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    category_image        = models.ImageField(upload_to="sub_category/",null=True,blank=True)
    description           = models.TextField(null=True,blank=True)

    def delete(self, *args, **kwargs):
        if self.category_image:
            if os.path.isfile(self.category_image.path):
                os.remove(self.category_image.path)
        super(SubCategory, self).delete(*args, **kwargs)
        
class Product(BaseModel):
    product_name         = models.CharField(max_length=128)
    sub_category         = models.ForeignKey(SubCategory,on_delete=models.CASCADE,null=True,blank=True)
    product_image        = models.ImageField(upload_to="product/",null=True,blank=True)
    price                = models.PositiveIntegerField()
    stock                = models.PositiveIntegerField()
    description          = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.product_name

        
    def delete(self, *args, **kwargs):
        if self.product_image:
            if os.path.isfile(self.product_image.path):
                os.remove(self.product_image.path)
        super(Product, self).delete(*args, **kwargs)