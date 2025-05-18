# from django.db import models
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# class UserProfile(models.Model):
#     GENDER_CHOICES = [
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('O', 'Other'),
#     ]

#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
#     bio = models.TextField(max_length=500, blank=True)
#     profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
#     nationality = models.CharField(max_length=100, blank=True)
#     province = models.CharField(max_length=100, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.first_name} {self.user.last_name}'s profile"

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s profile"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_user_profile(sender, instance, **kwargs):
    # will fetch the existing profile or create it if missing
    UserProfile.objects.get_or_create(user=instance)
