from django.db import models
from portals.models import BaseModel
import os 
# from accounts.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Category(BaseModel):
    category_name        = models.CharField(max_length=128)
    category_image       = models.ImageField(upload_to="category/",null=True,blank=True)
    category_description = models.TextField(null=True,blank=True)
    
    def delete(self, *args, **kwargs):
        if self.category_image:
            if os.path.isfile(self.category_image.path):
                os.remove(self.category_image.path)
        super(Category, self).delete(*args, **kwargs)
        
    def __str__(self):
        return self.category_name

class SubCategory(BaseModel):
    name                  = models.CharField(max_length=258)
    category              = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="subcategory",null=True,blank=True)
    category_image        = models.ImageField(upload_to="sub_category/",null=True,blank=True)
    description           = models.TextField(null=True,blank=True)

    def delete(self, *args, **kwargs):
        if self.category_image:
            if os.path.isfile(self.category_image.path):
                os.remove(self.category_image.path)
        super(SubCategory, self).delete(*args, **kwargs)
        
    def __str__(self):
        return self.name


class Store(BaseModel):
    store_admin    = models.OneToOneField("accounts.User",on_delete=models.CASCADE) 
    store_name     = models.CharField(max_length=256,default="Store 1")
    store_address  = models.CharField(max_length=256,null=True,blank=True)
    store_image    = models.ImageField(upload_to="stores/",null=True,blank=True)
    
    def __str__(self):
        return f"{self.store_name} - {self.store_admin.username}"
    

class StorePincode(models.Model):
    store   = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='pincodes')
    pincode = models.CharField(max_length=6)  
    def __str__(self):
        return self.pincode
    
class Product(BaseModel):
    product_name         = models.CharField(max_length=128,unique=True)
    sub_category         = models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name="products",null=True,blank=True)
    product_image        = models.ImageField(upload_to="product/",null=True,blank=True)
    price                = models.PositiveIntegerField()
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
    
@receiver(post_save, sender=Store)
def add_products_to_inventory(sender, instance, created, **kwargs):
    if created:
        products = Product.objects.all()
        for product in products:
            Inventory.objects.create(store=instance, product=product, stock=100)





