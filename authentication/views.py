# authentication/views.py
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, JWTSerializer, ProfileSerializer, VerifyEmailSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import Profile
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.exceptions import ValidationError
import random
from django.core.cache import cache  
from django.conf import settings
from rest_framework.generics import GenericAPIView


class RegisterView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({'access': access_token, 'refresh': refresh_token})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JWTTokenView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = JWTSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordRequestView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        email = request.data.get("email")
        if not email:
            raise ValidationError("Email is required.")

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            raise ValidationError("User with this email does not exist.")

        # Generate random OTP
        otp = str(random.randint(100000, 999999))

        # Save OTP in cache with a timeout of 10 minutes (600 seconds)
        cache.set(f"reset_otp_{user.pk}", otp, timeout=600)

        # Send OTP to user's email
        send_mail(
            subject="Password Reset OTP",
            message=f"Your OTP for password reset is: {otp}. It will expire in 10 minutes.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )

        return Response({"message": "OTP has been sent to your email."}, status=status.HTTP_200_OK)


class ResetPasswordView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        new_password = request.data.get("password")

        if not email or not otp or not new_password:
            raise ValidationError("Email, OTP, and Password are required.")

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            raise ValidationError("User with this email does not exist.")

        # Retrieve OTP from cache
        cached_otp = cache.get(f"reset_otp_{user.pk}")

        if cached_otp != otp:
            raise ValidationError("Invalid OTP.")

        # Set the new password
        user.set_password(new_password)
        user.save()

        # Delete the OTP from cache after successful reset
        cache.delete(f"reset_otp_{user.pk}")

        return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)


class IsProfileOwner(BasePermission):
    """
    Custom permission to only allow users to edit their own profile.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing profiles of authenticated users.
    Provides the ability to view and edit the profile.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_queryset(self):
        """
        Overriding to return only the authenticated user's profile.
        """
        return Profile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Automatically link the profile to the authenticated user when creating it.
        """
        serializer.save(user=self.request.user)

class VerifyEmailView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({
                'message': 'Email verified successfully. You can now login.'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)