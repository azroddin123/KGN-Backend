from django.contrib import admin
from .models import Cart, CartItem, Orders, OrderedItems

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'ordered', 'total_price')
    search_fields = ('user__username',)
    list_filter = ('ordered',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__user__username', 'product__product_name')
    list_filter = ('cart', 'product')

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_id', 'amount', 'is_paid', 'order_status', 'delivery_boy', 'delivery_time', 'created_on')
    search_fields = ('user__username', 'order_id', 'email', 'mobile_number')
    list_filter = ('is_paid', 'order_status', 'delivery_boy')

@admin.register(OrderedItems)
class OrderedItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__order_id', 'product__product_name')
    list_filter = ('order', 'product')

