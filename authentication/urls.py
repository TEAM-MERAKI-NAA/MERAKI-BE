# authentication/urls.py
from django.urls import path
from .views import (
    RegisterView, LoginView, JWTTokenView, 
    ProfileView, VerifyEmailView, ResendOTPView
)

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/', JWTTokenView.as_view(), name='token'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('api/resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
]