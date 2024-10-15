from django.db import models

# Create your models here.
from portals.models import BaseModel
from products.models import * 
from accounts.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from portals.choices import OrderChoices,PaymentStatusChoices

class Cart(BaseModel):
    user              = models.OneToOneField(User, related_name="user_cart", on_delete=models.CASCADE,null=True,blank=True)
    ordered           = models.BooleanField(default=False)
    total_price       = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    # def __str__(self):
    #     return str(self.user.username)+" "+ str(self.total_price)
    
@receiver(post_save, sender=User)
def create_user_cart(sender, created, instance, *args, **kwargs):
    if created:
        Cart.objects.create(user=instance)

class CartItem(BaseModel):
    cart      = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True,blank=True,related_name="cart_items")
    product   = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    quantity  = models.IntegerField(default=1)
    class Meta:
        unique_together = ('cart', 'product')


   
    

class Orders(BaseModel):
    user              = models.ForeignKey(User, on_delete=models.CASCADE)
    amount            = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    is_paid           = models.BooleanField(default=False)
    order_id          = models.CharField(max_length=100, null=True,blank=True)
    payment_id        = models.CharField(max_length=100, null=True,blank=True)
    payment_status    = models.CharField(max_length=100, null=True,blank=True)
    
    order_status      = models.CharField(max_length=20, choices=OrderChoices.choices, default=OrderChoices.PENDING)
    delivery_boy      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name="delivery_boy")
    store_id          = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True,blank=True)
    
    delivery_address  = models.TextField()
    delivery_cost     = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    delivery_time     = models.DateTimeField(null=True, blank=True)
    pincode           = models.CharField(max_length=10,null=True,blank=True)
    

class OrderedItems(BaseModel):
    order     = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    quantity  = models.IntegerField(default=0)
