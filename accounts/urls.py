from django.urls import path
from .views import * 

urlpatterns = [
    
    path('user',UserAPI.as_view()),
    path('user/<str:pk>', UserAPI.as_view()),
    path('verify-otp/nt/',VerifyOTPApi.as_view()),
    path('resend-otp/nt/',ResendOTPApi.as_view()),
    path('register/nt/',RegisterUserApi.as_view()),
    path('user/nt/',UserAPI.as_view()),
    path('login/nt/',LoginAPI.as_view()),
    path('user-profile',UserProfileAPI.as_view()),
    path('user-login/nt/',LoginWithUsernamePassword.as_view()),    
]