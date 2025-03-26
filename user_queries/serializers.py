from rest_framework import serializers
from .models import Category, Community, CommunityRequest

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'category', 'created_at', 'updated_at', 'image', 'members']

class CommunityRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityRequest
        fields = ['id', 'name', 'description', 'proposed_category', 'is_approved', 'created_at']
