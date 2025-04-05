# authentication/admin.py
from django.contrib import admin
from .models import CustomUser

# Register the custom User model and the Profile inline
admin.site.register(CustomUser)

