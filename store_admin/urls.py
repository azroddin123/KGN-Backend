from django.urls import path
from products.views import * 
from .views import * 
urlpatterns = [
    
    path('category',CategoryAPI.as_view()),
    path('category/<str:pk>',CategoryAPI.as_view()),
    
    path('sub-category',SubCategoryAPI.as_view()),
    path('sub-category/<str:pk>',SubCategoryAPI.as_view()),
    
    path('products',StoreProductAPI.as_view()),
    path('products/<str:pk>',StoreProductAPI.as_view()),
        
    # path('customers',CustomerAPI.as_view()),
    # path('customers/<str:pk>',CustomerAPI.as_view()),
    
    path('inventory',StoreInventoryAPI.as_view()),
    path('inventory/<str:pk>',StoreInventoryAPI.as_view()),
    
    path('store',StoreAPI.as_view()),
    path('store/<str:pk>',StoreAPI.as_view()),
    
    path('orders',StoreOrdersAPI.as_view()),
    path('orders/<str:pk>',StoreOrdersAPI.as_view()),
    
    
    path('add-store',AddStoreAPI.as_view()),
    path('add-store/<str:pk>',AddStoreAPI.as_view()),
    
    # Get All Delivery Man
    
    path('delivery-man', GetAllDeliveryMan.as_view()),
    path('assign-order/<str:pk>',AssignOrderAPI.as_view()),
    
    
      
]