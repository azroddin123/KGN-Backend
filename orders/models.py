from django.db import models

# Create your models here.
from portals.models import BaseModel
from products.models import * 
from accounts.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Cart(BaseModel):
    user              = models.OneToOneField(User, related_name="user_cart", on_delete=models.CASCADE,null=True,blank=True)
    ordered           = models.BooleanField(default=False)
    total_price       = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.user.username)+" "+ str(self.total_price)
    
@receiver(post_save, sender=User)
def create_user_cart(sender, created, instance, *args, **kwargs):
    if created:
        Cart.objects.create(user=instance)

class CartItem(BaseModel):
    cart      = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True,blank=True,related_name="cart")
    product   = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    quantity  = models.IntegerField(default=1)


class Orders(BaseModel):
    user              = models.ForeignKey(User, on_delete=models.CASCADE)
    cart              = models.ForeignKey(Cart, on_delete=models.CASCADE)
    amount            = models.FloatField(default=0)
    is_paid           = models.CharField(max_length=100, blank=True)
    order_id          = models.CharField(max_length=100, blank=True)
    payment_id        = models.CharField(max_length=100, blank=True)
    payment_signature = models.CharField(max_length=100, blank=True)

class OrderedItems(BaseModel):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
