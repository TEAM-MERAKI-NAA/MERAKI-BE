from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api/register-user/',
         views.UserRegisterAfterOtp.as_view(), name='user_registration'),
    path(r'api/validate-user/', views.ValidateOTP.as_view(), name='validate_user'),
    path(r'api/resend-otp/', views.ResendOTP.as_view(), name='resend_otp'),
    path(r'api/send-otp/', views.UserOtpRegistration.as_view(), name='send_otp'),
    path(r'api/verify-user-if-logged-in', views.VerifyUserIfLoggedIn.as_view(), name='verify_user'),
    path(r'api/fp-send-otp/', views.ForgotPasswordSendOtp.as_view(), name='forgot_password_send_otp'),
    path(r'api/fp-new-password/', views.ForgotPasswordAfterOtpVerify.as_view(),
         name='forgot_password_new_pass'),
]
