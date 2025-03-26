from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Category name
    description = models.TextField(blank=True, null=True)  # Optional description
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return self.name

class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Community name
    description = models.TextField(blank=True, null=True)  # Community description
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='communities')  # Link to category
    created_at = models.DateTimeField(auto_now_add=True)  # Community creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Auto-updated timestamp
    image = models.ImageField(upload_to='community_images/', blank=True, null=True)  # Optional image
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='communities')  # Members

    def __str__(self):
        return self.name

class CommunityRequest(models.Model):
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_requests')  # Requester
    name = models.CharField(max_length=100)  # Community name requested
    description = models.TextField(blank=True, null=True)  # Community description requested
    proposed_category = models.CharField(max_length=100, blank=True, null=True)  # Optional new category name
    is_approved = models.BooleanField(default=False)  # Approval status
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"Request: {self.name} by {self.requester.username}"
