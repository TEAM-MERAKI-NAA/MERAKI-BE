# from django.db import models
# from django.contrib.auth.models import User


# class Community(models.Model):
#     # Community Types
#     NATIONALITY = 'nationality'
#     PROVINCE = 'province'
#     FUNCTIONAL = 'functional'
#     COMMUNITY_TYPES = [
#         (NATIONALITY, 'Nationality-Based'),
#         (PROVINCE, 'Province-Based'),
#         (FUNCTIONAL, 'Functional'),
#     ]

#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True, null=True)
#     community_type = models.CharField(max_length=20, choices=COMMUNITY_TYPES, default=FUNCTIONAL)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)  # Automatically updated when community is saved
#     image = models.ImageField(upload_to='community_images/', blank=True, null=True)  # For community images
#     members = models.ManyToManyField(User, related_name='communities')  # Users belonging to the community

#     def __str__(self):
#         return self.name

# class CommunityRequest(models.Model):
#     requester = models.ForeignKey(User, related_name='community_requests', on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     proposed_category = models.CharField(max_length=100, blank=True, null=True)  # Optional new category
#     is_approved = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Request: {self.name} by {self.requester.username}"
from django.conf import settings  # Import settings to use AUTH_USER_MODEL
from django.db import models

class Community(models.Model):
    NATIONALITY = 'nationality'
    PROVINCE = 'province'
    FUNCTIONAL = 'functional'
    COMMUNITY_TYPES = [
        (NATIONALITY, 'Nationality-Based'),
        (PROVINCE, 'Province-Based'),
        (FUNCTIONAL, 'Functional'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    community_type = models.CharField(max_length=20, choices=COMMUNITY_TYPES, default=FUNCTIONAL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='community_images/', blank=True, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='communities')  # Updated

    def __str__(self):
        return self.name

class CommunityRequest(models.Model):
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='community_requests', on_delete=models.CASCADE)  # Updated
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    proposed_category = models.CharField(max_length=100, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request: {self.name} by {self.requester.username}"
