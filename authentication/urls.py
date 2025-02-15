from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api/register-user/',
         views.UserCreateViewSet.as_view(), name='user_registration'),
    path(r'api/validate-user/', views.ValidateOTP.as_view(), name='validate_user'),
    path(r'api/resend-otp/', views.ResendOTP.as_view(), name='resend_otp'),
    path(r'api/check_if_logged_in', views.CheckIfLoggedIn.as_view(), name='check_if_logged_in'),
    
]
