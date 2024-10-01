from django.db import models
from portals.models import BaseModel
import os 

from accounts.models import User
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


class Store(BaseModel):
    store_admin    = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True) 
    store_name     = models.CharField(max_length=256,null=True,blank=True)
    store_address  = models.CharField(max_length=256,null=True,blank=True)
    pincode        = models.CharField(max_length=6,null=True,blank=True)
    

class ServiceArea(BaseModel):
    store      = models.ForeignKey(Store,on_delete=models.CASCADE,null=True,blank=True)
    pincode    = models.CharField(max_length=6)
    area_name  = models.CharField(max_length=128)
    

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

class Inventory(models.Model):
    store        = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='inventory')
    product      = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory')
    stock        = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('store', 'product')

    def __str__(self):
        return f"{self.product.product_name} - {self.store.store_name} (Stock: {self.stock})"