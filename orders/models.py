from django.db import models

# Create your models here.
from portals.models import BaseModel
from products.models import * 
from accounts.models import User


class Cart(BaseModel):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered     = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.user.username) + " "+ str(self.total_price)

class CartItem(BaseModel):
    cart      = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    price     = models.FloatField(default=0)
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
