# authentication/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
import random
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'is_verified')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password', 'password2', 'is_verified')
        extra_kwargs = {
            'email': {'required': True},
            'phone_number': {'required': False},
            'is_verified': {'read_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')
        
        try:
            user = User.objects.get(email=email)
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
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_verified:
            raise serializers.ValidationError("Please verify your email before logging in")
        return {"user": user}

class JWTSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

    def create(self, validated_data):
        refresh = validated_data.get('refresh')
        access = validated_data.get('access')
        return {'refresh': refresh, 'access': access}

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture', 'nationality', 'province', 'gender', 'first_name', 'last_name')

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.nationality = validated_data.get('nationality', instance.nationality)
        instance.province = validated_data.get('province', instance.province)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

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
