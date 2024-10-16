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
    name              = models.CharField(max_length=128,null=True,blank=True)
    city              = models.CharField(max_length=128,null=True,blank=True)
    mobile_number     = models.CharField(max_length=10,null=True,blank=True)
    is_paid           = models.BooleanField(default=False)
    order_id          = models.CharField(max_length=100, null=True,blank=True)
    payment_id        = models.CharField(max_length=100, null=True,blank=True)
    payment_status    = models.CharField(max_length=100, null=True,blank=True)
    
    order_status      = models.CharField(max_length=20, choices=OrderChoices.choices, default=OrderChoices.PENDING)
    delivery_boy      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name="delivery_boy")
    store_id          = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True,blank=True)
    
    payment_type      = models.CharField(max_length=128,default="COD")
    delivery_address  = models.TextField()
    delivery_cost     = models.DecimalField(max_digits=8, decimal_places=2, default=50.00)
    delivery_time     = models.DateTimeField(null=True, blank=True)
    pincode           = models.CharField(max_length=10,null=True,blank=True)
    notes             = models.TextField(null=True,blank=True)  

class OrderedItems(BaseModel):
    order     = models.ForeignKey(Orders, on_delete=models.CASCADE,related_name="ordered_items")
    product   = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    quantity  = models.IntegerField(default=0)


class Invoice(BaseModel):
    booking        = models.OneToOneField(Orders, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=100, unique=True)
    invoice_date   = models.DateField(auto_now_add=True)
    due_date       = models.DateField()
    total_amount   = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50,default="CASH")
    transaction_id = models.CharField(max_length=100, unique=True,null=True,blank=True)
    payment_status = models.CharField(max_length=50, choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'),("FAILED","Failed")], default='PENDING')
    notes          = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-invoice_date']

    def save(self, *args, **kwargs):
        # Auto-generate invoice number if not set
        if not self.invoice_number:
            last_invoice = Invoice.objects.order_by('created_on').last()
            if last_invoice:
                print(last_invoice,"last_invoice----------")
                # Extract the number part from the last invoice_number and increment it
                last_invoice_number = int(last_invoice.invoice_number.replace('INV', ''))
                self.invoice_number = f'INV{last_invoice_number + 1:04d}'
            else:
                self.invoice_number = 'INV0001'
        super().save(*args, **kwargs)
