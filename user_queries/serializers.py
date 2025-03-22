from rest_framework import serializers
from .models import Community, CommunityRequest

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'community_type', 'created_at', 'updated_at', 'image', 'members']

class CommunityRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityRequest
        fields = ['id', 'name', 'description', 'proposed_category', 'is_approved', 'created_at']
