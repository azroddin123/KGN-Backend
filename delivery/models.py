from django.db import models
from accounts.models import User
# Create your models here.

class DeliveryMan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="delivery_man_profile")
    vehicle_number = models.CharField(max_length=50, null=True, blank=True)  # For tracking delivery vehicle
    driving_license = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_available = models.BooleanField(default=True)  
    current_order = models.OneToOneField('Orders', on_delete=models.SET_NULL, null=True, blank=True)  # If assigned to an active order
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)  # Average rating by customers
    joined_on = models.DateTimeField(auto_now_add=True)  
    updated_on = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.user.username} - Delivery Man"