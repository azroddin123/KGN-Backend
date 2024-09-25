from django.db import models

# Create your models here.
from portals.models import BaseModel
from products.models import * 
from accounts.models import User


class Cart(BaseModel):
    pass

class CartItem(BaseModel):
    pass  

class Order(BaseModel):
    pass

class Payment(BaseModel):
    pass
