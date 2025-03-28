from rest_framework import serializers
from django.conf import settings
from .models import Community, CommunityRequest, Post, Comment, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']


class CommunitySerializer(serializers.ModelSerializer):
    # Optionally, if you want nested category representation, uncomment the line below:
    # category = CategorySerializer(read_only=True)
    # Otherwise, you may use a primary key representation:
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'category', 'created_at', 'updated_at', 'image', 'is_approved', 'members_count']


class CommunityRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityRequest
        # Note: Use "status" as defined in the model, not "is_approved"
        fields = ['id', 'name', 'description', 'proposed_category', 'status', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    # Using PrimaryKeyRelatedField (read-only) for community and author for simplicity.
    community = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Post
        # Include the "title" field since it is part of the Post model.
        fields = ['id', 'community', 'author', 'title', 'content', 'image', 'created_at', 'upvotes', 'downvotes']


class CommentSerializer(serializers.ModelSerializer):
    # For parent, post, and author, we'll represent them by primary keys for simplicity.
    parent = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'image', 'created_at', 'parent', 'upvotes', 'downvotes']
