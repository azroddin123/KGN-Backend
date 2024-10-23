from django.urls import path
from .views import * 

urlpatterns = [
    path('create-profile',DeliveryManAPI.as_view()),
    path('create-profile/<str:pk>',DeliveryManAPI.as_view())
    
]