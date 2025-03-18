# authentication/views.py
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer, LoginSerializer, JWTSerializer, 
    ProfileSerializer, VerifyEmailSerializer, ResendOTPSerializer
)
from django.contrib.auth import get_user_model
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import ValidationError
import random
from django.core.cache import cache

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Registration successful. Please check your email for OTP verification.',
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({'access': access_token, 'refresh': refresh_token})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JWTTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = JWTSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return None

    def perform_create(self, serializer):
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

class ResendOTPView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResendOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            # Generate new OTP
            otp = str(random.randint(100000, 999999))
            
            # Save OTP in cache with 10 minutes timeout
            cache.set(f"registration_otp_{email}", otp, timeout=600)
            
            # Send OTP via email
            send_mail(
                subject='Verify your email with OTP',
                message=f'Your new OTP for email verification is: {otp}. It will expire in 10 minutes.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            
            return Response({
                "message": "New OTP has been sent to your email."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)