from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta, datetime
from django.core.mail import send_mail
from django.conf import settings
from .models import Income, ExpenseCategory, Expense, BudgetRecommendation, FinancialSummary
from .serializers import (
    IncomeSerializer, ExpenseCategorySerializer, ExpenseSerializer,
    BudgetRecommendationSerializer, FinancialSummarySerializer
)

# Create your views here.

class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary_by_category(self, request):
        expenses = self.get_queryset()
        summary = expenses.values('category__name').annotate(total=Sum('amount'))
        return Response(summary)

class BudgetRecommendationViewSet(viewsets.ModelViewSet):
    queryset = BudgetRecommendation.objects.all()
    serializer_class = BudgetRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_recommendations(self, request):
        category_id = request.query_params.get('category')
        if category_id:
            recommendations = self.queryset.filter(category_id=category_id)
        else:
            recommendations = self.queryset.all()
        serializer = self.get_serializer(recommendations, many=True)
        return Response(serializer.data)

class FinancialSummaryViewSet(viewsets.ModelViewSet):
    serializer_class = FinancialSummarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FinancialSummary.objects.filter(user=self.request.user)

    def calculate_summary(self, start_date, end_date):
        incomes = Income.objects.filter(
            user=self.request.user,
            date__range=[start_date, end_date]
        )
        expenses = Expense.objects.filter(
            user=self.request.user,
            date__range=[start_date, end_date]
        )

        total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        remaining_balance = total_income - total_expenses

        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'remaining_balance': remaining_balance
        }

    @action(detail=False, methods=['get'])
    def generate_summary(self, request):
        period = request.query_params.get('period', 'monthly')
        today = timezone.now().date()

        if period == 'weekly':
            start_date = today - timedelta(days=7)
        elif period == 'biweekly':
            start_date = today - timedelta(days=14)
        else:  # monthly
            start_date = today - timedelta(days=30)

        summary = self.calculate_summary(start_date, today)
        
        # Create or update the financial summary
        financial_summary, created = FinancialSummary.objects.update_or_create(
            user=self.request.user,
            start_date=start_date,
            end_date=today,
            defaults={
                'total_income': summary['total_income'],
                'total_expenses': summary['total_expenses'],
                'remaining_balance': summary['remaining_balance']
            }
        )

        serializer = self.get_serializer(financial_summary)
        return Response(serializer.data)

def send_expense_reminder_email(user_email):
    """
    Send a daily reminder email to users to log their expenses
    """
    subject = 'Daily Expense Tracking Reminder'
    message = '''
    Hello!
    
    This is your daily reminder to log your expenses for today. 
    Keeping track of your expenses helps you maintain better control of your finances.
    
    Don't forget to:
    - Log any purchases you made today
    - Categorize your expenses
    - Check your remaining budget
    
    Best regards,
    Your Budget Tracker Team
    '''
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )

class CurrentMonthSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        total_income = Income.objects.filter(
            user=request.user,
            date__gte=start_of_month,
            date__lte=now
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_expenses = Expense.objects.filter(
            user=request.user,
            date__gte=start_of_month,
            date__lte=now
        ).aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_savings': total_income - total_expenses,
            'period_start': start_of_month,
            'period_end': now
        })

class SpendingByCategoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        expenses_by_category = Expense.objects.filter(
            user=request.user,
            date__gte=start_of_month
        ).values('category__name').annotate(
            total=Sum('amount')
        ).order_by('-total')

        return Response(expenses_by_category)

class MonthlyTrendsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        six_months_ago = now - timedelta(days=180)
        
        monthly_expenses = Expense.objects.filter(
            user=request.user,
            date__gte=six_months_ago
        ).values('date__year', 'date__month').annotate(
            total=Sum('amount')
        ).order_by('date__year', 'date__month')

        monthly_income = Income.objects.filter(
            user=request.user,
            date__gte=six_months_ago
        ).values('date__year', 'date__month').annotate(
            total=Sum('amount')
        ).order_by('date__year', 'date__month')

        return Response({
            'expenses': monthly_expenses,
            'income': monthly_income
        })

class BudgetRecommendationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        three_months_ago = now - timedelta(days=90)

        # Calculate average monthly income
        avg_monthly_income = Income.objects.filter(
            user=request.user,
            date__gte=three_months_ago
        ).aggregate(avg=Sum('amount') / 3)['avg'] or 0

        # Calculate average spending by category
        avg_spending_by_category = Expense.objects.filter(
            user=request.user,
            date__gte=three_months_ago
        ).values('category__name').annotate(
            avg_amount=Sum('amount') / 3
        ).order_by('-avg_amount')

        # Generate recommendations
        recommendations = []
        total_avg_expenses = sum(item['avg_amount'] for item in avg_spending_by_category)
        
        if total_avg_expenses > avg_monthly_income * 0.9:
            recommendations.append({
                'type': 'warning',
                'message': 'Your expenses are close to or exceeding your income. Consider reducing expenses.'
            })

        for category in avg_spending_by_category:
            if category['avg_amount'] > avg_monthly_income * 0.3:
                recommendations.append({
                    'type': 'suggestion',
                    'message': f"Your spending in {category['category__name']} is relatively high "
                             f"({(category['avg_amount'] / avg_monthly_income * 100):.1f}% of income). "
                             "Consider setting a lower budget for this category."
                })

        return Response({
            'average_monthly_income': avg_monthly_income,
            'average_monthly_expenses': total_avg_expenses,
            'spending_by_category': avg_spending_by_category,
            'recommendations': recommendations
        })
