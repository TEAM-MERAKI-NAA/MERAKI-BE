from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'first_name', 'last_name', 'bio', 
                 'profile_image', 'gender', 'nationality', 'province', 
                 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] 