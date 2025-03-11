from rest_framework import serializers
from .models import *
from authentication.serializers import UserProfileSerializer


class MyProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model=MyProfile
        fields=('user_id', 'image', 'user', 'status_in_canada', 'describe_you')

class MyProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyProfile
        fields=('image',)
 
