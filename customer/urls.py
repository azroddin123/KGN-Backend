from django.urls import path,include
from .views import * 
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from orders.views import * 
router = DefaultRouter()
router.register(r'products-filter', ProductViewSet) 

urlpatterns = [
    path('category',CategoryAPI.as_view()),
    path('category/<str:pk>',CategoryAPI.as_view()),
    
    path('sub-category',SubCategoryAPI.as_view()),
    path('sub-category/<str:pk>',SubCategoryAPI.as_view()),
    
    path('products',ProductAPI.as_view()),
    path('products/<str:pk>',ProductAPI.as_view()),
    
    path('all-categories',GetSubcategoriesAPI.as_view()),
    path('all-products',GetAllProductsBySubCategoryAPI.as_view()),
    
    path('main-category',GetCategoriesWithSubCategoriesAPI.as_view()),
    path('subcategory-products',ProductsListWithSubcategoriesAPI.as_view()),
    
    path('cart',CartAPI.as_view()),
    path('cart/<str:pk>',CartAPI.as_view()),
    
    path('', include(router.urls)),
    
]