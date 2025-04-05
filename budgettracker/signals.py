# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils import timezone
# from django.db import models
# from .models import Expense, FinancialSummary, Income

# def update_monthly_summary(user):
#     """
#     Update or create the financial summary for the current month
#     """
#     today = timezone.now().date()
#     start_date = today.replace(day=1)  # First day of current month
    
#     summary, _ = FinancialSummary.objects.get_or_create(
#         user=user,
#         start_date=start_date,
#         end_date=today,
#         defaults={
#             'total_income': 0,
#             'total_expenses': 0,
#             'remaining_balance': 0
#         }
#     )
    
#     # Recalculate totals
#     expenses = Expense.objects.filter(
#         user=user,
#         date__range=[start_date, today]
#     ).aggregate(total=models.Sum('amount'))
    
#     income = Income.objects.filter(
#         user=user,
#         date__range=[start_date, today]
#     ).aggregate(total=models.Sum('amount'))
    
#     summary.total_expenses = expenses['total'] or 0
#     summary.total_income = income['total'] or 0
#     summary.remaining_balance = summary.total_income - summary.total_expenses
#     summary.save()

# @receiver(post_save, sender=Expense)
# def update_financial_summary_expense(sender, instance, created, **kwargs):
#     """
#     Update financial summary when a new expense is created or updated
#     """
#     if created or instance.date >= timezone.now().date() - timezone.timedelta(days=30):
#         update_monthly_summary(instance.user)

# @receiver(post_save, sender=Income)
# def update_financial_summary_income(sender, instance, created, **kwargs):
#     """
#     Update financial summary when a new income is created or updated
#     """
#     if created or instance.date >= timezone.now().date() - timezone.timedelta(days=30):
#         update_monthly_summary(instance.user) 