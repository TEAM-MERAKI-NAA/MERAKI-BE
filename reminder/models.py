from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import datetime

User = get_user_model()

class Reminder(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=200)
    document_expiry_date = models.DateField()
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    last_reminder_sent = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.email}"

    def should_send_reminder(self):
        if not self.is_active:
            return False

        if not self.last_reminder_sent:
            return True

        now = timezone.now()
        last_sent = self.last_reminder_sent

        if self.frequency == 'daily':
            return (now - last_sent).days >= 1
        elif self.frequency == 'weekly':
            return (now - last_sent).days >= 7
        elif self.frequency == 'monthly':
            return (now - last_sent).days >= 30
        elif self.frequency == 'yearly':
            return (now - last_sent).days >= 365

        return False
