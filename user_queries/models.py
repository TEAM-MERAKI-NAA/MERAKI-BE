from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Category name
    description = models.TextField(blank=True, null=True)  # Optional description
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp
    members = models.ManyToManyField(User, related_name="joined_communities")

    def __str__(self):
        return self.name

class Community(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    members_count = models.IntegerField(default=0)  # Add this field
    name = models.CharField(max_length=100, unique=True)  # Community name
    description = models.TextField(blank=True, null=True)  # Community description
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='communities')  # Link to category
    created_at = models.DateTimeField(auto_now_add=True)  # Community creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Auto-updated timestamp
    image = models.ImageField(upload_to='community_images/', blank=True, null=True)  # Optional image
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='communities')  # Members

    def __str__(self):
        return self.name

class CommunityMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

class Post(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # Field for images
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)  # Field for images
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

class CommunityRequest(models.Model):
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_requests')  # Requester
    name = models.CharField(max_length=100)  # Community name requested
    description = models.TextField(blank=True, null=True)  # Community description requested
    proposed_category = models.CharField(max_length=100, blank=True, null=True)  # Optional new category name
    is_approved = models.BooleanField(default=False)  # Approval status
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"Request: {self.name} by {self.requester.username}"
