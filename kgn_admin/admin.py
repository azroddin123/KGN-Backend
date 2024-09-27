from django.contrib import admin

# Register your models here.
from products.models import * 
from accounts.models import * 
from orders.models import * 

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)


admin.site.register(Orders)
admin.site.register(OrderedItems)
admin.site.register(Cart)
admin.site.register(CartItem)