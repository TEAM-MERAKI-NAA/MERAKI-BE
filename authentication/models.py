# authentication/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(unique=True, max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=15, blank=True, null=True)
    nationality = models.CharField(max_length=15, blank=True, null=True)
    province = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    first_name = models.CharField(max_length=15, blank=True, null=True)
    last_name = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.email}"
