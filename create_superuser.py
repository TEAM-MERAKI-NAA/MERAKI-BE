import os
from django.contrib.auth import get_user_model

# Retrieve the environment variables for the superuser
email = os.getenv('DJANGO_SUPERUSER_EMAIL')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
confirm_password = os.getenv('DJANGO_SUPERUSER_PASSWORD_CONFIRM')

# Check if the password and confirm password match
if password != confirm_password:
    print("Error: Password and confirm password do not match.")
    exit(1)

# Create the superuser if it doesn't already exist
User = get_user_model()
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)
    print(f"Superuser created with email: {email}")
else:
    print(f"Superuser already exists with email: {email}")
