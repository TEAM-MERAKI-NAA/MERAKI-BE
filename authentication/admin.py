from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'password')}),
        (_('Personal info'), {
         'fields': ('first_name', 'last_name', 'user_type')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','phone_number', 'password1', 'password2'),
        }),
    )
    list_display = ('username','email','phone_number', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone_number',
                     'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User)