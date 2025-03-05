from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.db import transaction
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        if not extra_fields.get('username'):
            raise ValueError('Users must have a valid username.')
        if not extra_fields.get('phone_number'):
            raise ValueError('Users must have a valid phone number.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# model utils - pypi
class User(AbstractUser):
    USER_TYPES = (
        (1, "General User"),
        (2, "Admin"),
    )
    username = models.CharField(max_length=50, unique=False, blank=True, null=True)
    email = models.EmailField(_('Email Address'), unique=True, blank=False, error_messages={'unique':"Email has already been registered."})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=30,  unique=True, error_messages={'unique':"Phone Number has already been registered."})
    user_type = models.IntegerField(choices=USER_TYPES, null=True, default=1)
    otp = models.IntegerField(null=True, blank=True)
    activation_key = models.CharField(max_length=150,blank=True,null=True)
    REQUIRED_FIELDS = ['username', 'phone_number', 'user_type']
    objects = UserManager()

    USERNAME_FIELD = 'email'


    def __unicode__(self):
        return self.username

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    data = reset_password_token.key

    send_mail(
        # title:
        "Password Reset for {title}".format(title="ImmigrationHub"),
        # message:
        "Kindly use this token to reset your password:     " + data,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email],
    )
