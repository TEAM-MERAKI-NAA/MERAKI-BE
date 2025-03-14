# authentication/admin.py
from django.contrib import admin
from .models import CustomUser, Profile
from django.contrib.auth.admin import UserAdmin


# Register Profile model as inline within the User model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Extending the UserAdmin to include Profile information
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

# Register the custom User model and the Profile inline
admin.site.register(CustomUser, CustomUserAdmin)

