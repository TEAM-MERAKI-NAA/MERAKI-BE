from rest_framework import serializers
from .models import Reminder

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['id', 'title', 'document_expiry_date', 'frequency', 'created_at', 'last_reminder_sent', 'is_active']
        read_only_fields = ['created_at', 'last_reminder_sent']

    def validate_document_expiry_date(self, value):
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("Document expiry date cannot be in the past")
        return value 