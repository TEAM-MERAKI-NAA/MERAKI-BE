from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from authentication.models import User
from .models import MyProfile


# class MyProfile(User):
#     class Meta:
#         proxy = True


# class MemberInline(admin.StackedInline):
#     model = MyProfile
#     can_delete = False
#     can_add = False
#     verbose_name_plural = 'profile'


# class MyUserAdmin(admin.ModelAdmin):
#     inlines = (MemberInline,)
#     verbose_name_plural = 'Members'

#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'phone_number', 'password')}),
#         (_('Personal info'), {
#          'fields': ('first_name', 'last_name', 'user_type')}),
#  )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'phone_number', 'password1', 'password2'),
#         }),
#     )
#     list_display = ('username', 'email', 'phone_number', 'first_name',
#                     'last_name', 'user_type', 'is_active')
#     search_fields = ('username', 'email', 'phone_number',
#                      'first_name', 'last_name')
#     ordering = ('email',)

# admin.site.register(MyProfile, MyUserAdmin)

