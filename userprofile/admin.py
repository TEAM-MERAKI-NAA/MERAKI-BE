from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'gender', 'nationality', 'province', 'created_at', 'updated_at')
    list_filter = ('gender', 'nationality', 'province', 'created_at')
    search_fields = ('user__username', 'user__email', 'first_name', 'last_name', 'nationality', 'province')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'first_name', 'last_name')
        }),
        ('Profile Details', {
            'fields': ('bio', 'profile_image', 'gender', 'nationality', 'province')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('user',)
        return self.readonly_fields
