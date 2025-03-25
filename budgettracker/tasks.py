from django.contrib.auth import get_user_model
from django.utils import timezone
from .views import send_expense_reminder_email

def send_daily_expense_reminders():
    """
    Send daily reminder emails to all users to log their expenses
    """
    User = get_user_model()
    users = User.objects.filter(is_active=True)
    
    for user in users:
        if user.email:
            send_expense_reminder_email(user.email) 