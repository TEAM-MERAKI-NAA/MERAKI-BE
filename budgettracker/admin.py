from django.contrib import admin
from .models import Income, ExpenseCategory, Expense, BudgetRecommendation, FinancialSummary

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'frequency', 'date')
    list_filter = ('frequency', 'date')
    search_fields = ('user__username', 'description')

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'date')
    list_filter = ('category', 'date')
    search_fields = ('user__username', 'description')

@admin.register(BudgetRecommendation)
class BudgetRecommendationAdmin(admin.ModelAdmin):
    list_display = ('category', 'tip_title', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('tip_title', 'description')

@admin.register(FinancialSummary)
class FinancialSummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'total_income', 'total_expenses', 'remaining_balance')
    list_filter = ('start_date', 'end_date')
    search_fields = ('user__username',)
