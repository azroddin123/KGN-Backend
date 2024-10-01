from django.urls import path
from .views import * 

urlpatterns = [
    path('category',CategoryAPI.as_view()),
    path('category/<str:pk>',CategoryAPI.as_view()),
    
    path('sub-category',SubCategoryAPI.as_view()),
    path('sub-category/<str:pk>',SubCategoryAPI.as_view()),
    
    path('products',ProductAPI.as_view()),
    path('products/<str:pk>',ProductAPI.as_view()),
    
    
    path('all-categories',GetSubcategoriesAPI.as_view()),
    path('all-products',GetAllProductsBySubCategoryAPI.as_view())
    
]