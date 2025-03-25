from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Expense, FinancialSummary

@receiver(post_save, sender=Expense)
def update_financial_summary(sender, instance, created, **kwargs):
    """
    Update financial summary when a new expense is created or updated
    """
    if created or instance.date >= timezone.now().date() - timezone.timedelta(days=30):
        # Get or create the current month's summary
        today = timezone.now().date()
        start_date = today.replace(day=1)  # First day of current month
        
        summary, _ = FinancialSummary.objects.get_or_create(
            user=instance.user,
            start_date=start_date,
            end_date=today,
            defaults={
                'total_income': 0,
                'total_expenses': 0,
                'remaining_balance': 0
            }
        )
        
        # Recalculate totals
        expenses = Expense.objects.filter(
            user=instance.user,
            date__range=[start_date, today]
        ).aggregate(total=models.Sum('amount'))
        
        summary.total_expenses = expenses['total'] or 0
        summary.remaining_balance = summary.total_income - summary.total_expenses
        summary.save() 