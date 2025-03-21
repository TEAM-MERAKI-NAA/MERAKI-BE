from django.contrib import admin
from .models import Reminder

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'document_expiry_date', 'frequency', 'created_at', 'last_reminder_sent', 'is_active')
    list_filter = ('frequency', 'is_active', 'created_at', 'document_expiry_date')
    search_fields = ('title', 'user__email', 'user__username')
    readonly_fields = ('created_at', 'last_reminder_sent')
    ordering = ('-created_at',)
    date_hierarchy = 'document_expiry_date'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
