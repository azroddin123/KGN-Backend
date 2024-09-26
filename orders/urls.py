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
]