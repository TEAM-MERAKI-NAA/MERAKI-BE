# authentication/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, LoginView, JWTTokenView, 
    ForgotPasswordRequestView, ResetPasswordView, 
    ProfileViewSet, VerifyEmailView
)

router = DefaultRouter()
router.register('register', RegisterView, basename='register')
router.register('login', LoginView, basename='login')
router.register('token', JWTTokenView, basename='token')
router.register('profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('api/forgot-password/', ForgotPasswordRequestView.as_view({'post': 'create'}), name='forgot-password'),
    path('api/reset-password/', ResetPasswordView.as_view({'post': 'create'}), name='reset-password'),
]