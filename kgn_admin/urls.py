from django.urls import path
from .views import * 
from products.views import * 
from accounts.views import UserAPI,CustomerAPI

urlpatterns = [
    
    path('category',CategoryAPI.as_view()),
    path('category/<str:pk>',CategoryAPI.as_view()),
    
    path('sub-category',SubCategoryAPI.as_view()),
    path('sub-category/<str:pk>',SubCategoryAPI.as_view()),
    
    path('products',ProductAPI.as_view()),
    path('products/<str:pk>',ProductAPI.as_view()),
        
    path('customers',CustomerAPI.as_view()),
    path('customers/<str:pk>',CustomerAPI.as_view()),
    
    path('inventory',InventoryAPI.as_view()),
    path('inventory/<str:pk>',InventoryAPI.as_view()),
    
    path('store',StoreAPI.as_view()),
    path('store/<str:pk>',StoreAPI.as_view()),
      
]