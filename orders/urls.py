from django.urls import path
from .views import * 

urlpatterns = [
    path('cart',CartAPI.as_view()),
    path('cart/<str:pk>',CartAPI.as_view()),
    
    path('cart-item',CartItemAPI.as_view()),
    path('cart-item/<str:pk>',CartItemAPI.as_view()),
    
    path('orders',OrdersAPI.as_view()),
    path('orders/<str:pk>',OrdersAPI.as_view()),
    
    path('order-items',OrderedItemAPI.as_view()),
    path('order-items/<str:pk>',OrderedItemAPI.as_view()),
    
    path('add-cart',AddItemToCartAPI.as_view()),
    path('place-order',OrderPaymentAPI.as_view()),
    # path('order-payment',OrderPaymentAPI.as_view()),
    
    path('my-cart',CustomerCartItemAPI.as_view()),
    path('my-cart/<str:pk>',CustomerCartItemAPI.as_view()),
    
    path('my-orders',CustomerOrdersAPI.as_view()),
    path('my-orders/<str:pk>',CustomerOrdersAPI.as_view())
    
]