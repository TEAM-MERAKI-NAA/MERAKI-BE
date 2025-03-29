# from django.db import models
# from django.conf import settings

# class Category(models.Model):
#     name = models.CharField(max_length=100, unique=True, db_index=True)
#     description = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# class Community(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True, null=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='communities')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     image = models.ImageField(upload_to='community_images/', blank=True, null=True)
#     is_approved = models.BooleanField(default=False)
#     members_count = models.IntegerField(default=0)

#     def __str__(self):
#         return f"{self.name} ({self.category.name})"


# class CommunityMembership(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='memberships')
#     joined_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['user', 'community'], name='unique_membership')
#         ]


# class Post(models.Model):
#     community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts')
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     image = models.ImageField(upload_to='post_images/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     upvotes = models.IntegerField(default=0, db_index=True)
#     downvotes = models.IntegerField(default=0, db_index=True)

#     def __str__(self):
#         return self.title


# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     content = models.TextField()
#     image = models.ImageField(upload_to='comment_images/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
#     upvotes = models.IntegerField(default=0, db_index=True)
#     downvotes = models.IntegerField(default=0, db_index=True)

#     def save(self, *args, **kwargs):
#         # Limit nested replies to one level.
#         if self.parent and self.parent.parent:
#             raise ValueError("Nested replies are limited to 1 level.")
#         super().save(*args, **kwargs)

#     def __str__(self):
#         # Return the first 50 characters of the content.
#         return self.content[:50]


# class CommunityRequest(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]
#     requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_requests')
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     proposed_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Request: {self.name} by {self.requester.username} - {self.status}"
from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings


class Category(models.Model):
    TYPE_CHOICES = [
        ('Province', 'Province'),
        ('Nationality', 'Nationality'),
        ('Functional', 'Functional'),
        ('Other', 'Other'), 
    ]
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=50, null=True, blank=True, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_predefined = models.BooleanField(default=False)
    image = models.ImageField(upload_to='communities/', null=True, blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.user.username} in {self.community.name}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s comment on Post {self.post.id}"

# class CommunityRequest(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     requested_name = models.CharField(max_length=100)
#     requested_category = models.CharField(max_length=100, null=True, blank=True)
#     new_category = models.BooleanField(default=False)
#     description = models.TextField()

#     def __str__(self):
#         return f"Request by {self.user.username}: {self.requested_name}"
class CommunityRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    requested_name = models.CharField(max_length=100)  # Name of the community
    requested_category = models.CharField(max_length=100, null=True, blank=True)  # Proposed category name
    new_category = models.BooleanField(default=False)  # Indicates if the request includes a new category
    description = models.TextField()  # Description of the new community

    def __str__(self):
        return f"Request by {self.user.username}: {self.requested_name}"

