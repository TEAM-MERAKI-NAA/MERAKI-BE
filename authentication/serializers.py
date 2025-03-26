# authentication/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
import random
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'first_name', 'last_name', 'is_verified')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password', 'password2', 'is_verified', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'phone_number': {'required': False},
            'is_verified': {'read_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Create user but don't save yet
        user = User(
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number', ''),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.is_active = False  # User won't be able to login until verified
        user.is_verified = False
        user.save()
        
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        
        # Save OTP in cache with 10 minutes timeout
        cache.set(f"registration_otp_{user.email}", otp, timeout=600)
        
        # Send OTP via email
        send_mail(
            subject='Verify your email with OTP',
            message=f'Your OTP for email verification is: {otp}. It will expire in 10 minutes.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        return user

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')
        
        try:
            user = User.objects.get(email=email)
            print(f"Found user: {user.email}, is_verified: {user.is_verified}, is_active: {user.is_active}")
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
            
        cached_otp = cache.get(f"registration_otp_{email}")
        
        if not cached_otp:
            raise serializers.ValidationError("OTP has expired")
            
        if cached_otp != otp:
            raise serializers.ValidationError("Invalid OTP")
            
        # If OTP is valid, activate the user
        user.is_active = True
        user.is_verified = True
        user.save()
        
        # Delete the OTP from cache
        cache.delete(f"registration_otp_{email}")
        
        return data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        
        try:
            user = User.objects.get(email=email)
            if not user.is_verified:
                raise serializers.ValidationError("Please verify your email before logging in")
            if not user.is_active:
                raise serializers.ValidationError("Your account is inactive")
                
            user = authenticate(username=email, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid credentials")
                
            return {"user": user}
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

class JWTSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

    def create(self, validated_data):
        refresh = validated_data.get('refresh')
        access = validated_data.get('access')
        return {'refresh': refresh, 'access': access}

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email')
        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                raise serializers.ValidationError("Email is already verified")
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        return data
