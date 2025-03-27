from rest_framework import serializers
from .models import Community, CommunityRequest,Post,Comment, Category

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'community_type', 'created_at', 'updated_at', 'image', 'members']

class CommunityRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityRequest
        fields = ['id', 'name', 'description', 'proposed_category', 'is_approved', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'community', 'author', 'content', 'image', 'created_at', 'upvotes', 'downvotes']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'image', 'created_at', 'upvotes', 'downvotes']
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']