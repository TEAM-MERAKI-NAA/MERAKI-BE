from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.db import transaction

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        if not extra_fields.get('username'):
            raise ValueError('Users must have a valid username.')
        # email = ''
        phone_number = ''
        data = {}
        username = email
        if '@' in username:
            email = self.normalize_email(username)
            data['email'] = email
            data['username'] = username
        else:
            phone_number = username
            data['phone_number'] = username
            data['username'] = username
        email = self.normalize_email(email)
        user = self.model(**data)
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
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


class User(AbstractUser):
    USER_TYPES = (
        (1, "General User"),
        (1, "Admin"),
    )
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(_('Email Address'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=30,  unique=False, blank=True, null=True)
    user_type = models.IntegerField(choices=USER_TYPES, null=True, default=1)
    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


    def __unicode__(self):
        return self.username

    @property
    def user_name(self):
        return self.email



class UserOtp(models.Model):
    username = models.CharField(max_length=100, unique=True)
    otp = models.IntegerField(null=True, blank=True)
    activation_key = models.CharField(max_length=150, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of OTP sent')
    validated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)
