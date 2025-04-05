from django.contrib import admin
from .models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'monthly_income', 'category', 'amount', 'description', 'date', 'remaining_amount')
    list_filter = ('category', 'date', 'user')
    search_fields = ('description', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'remaining_amount')
    ordering = ('-date', '-created_at')

# Commented out old admin registrations
'''
@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'frequency', 'description', 'date')
    list_filter = ('frequency', 'date', 'user')
    search_fields = ('description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date', '-created_at')

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'description', 'date')
    list_filter = ('category', 'date', 'user')
    search_fields = ('description', 'user__username', 'category__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date', '-created_at')

@admin.register(BudgetRecommendation)
class BudgetRecommendationAdmin(admin.ModelAdmin):
    list_display = ('category', 'tip_title', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('tip_title', 'description', 'category__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(FinancialSummary)
class FinancialSummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'total_income', 'total_expenses', 'remaining_balance')
    list_filter = ('start_date', 'end_date', 'user')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-end_date', '-created_at')

@admin.register(UserMonthlyBudget)
class UserMonthlyBudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'monthly_income', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(BudgetCategory)
class BudgetCategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'is_fixed', 'created_at')
    list_filter = ('is_fixed', 'created_at', 'user')
    search_fields = ('name', 'user__username')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(BudgetExpense)
class BudgetExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'description', 'date')
    list_filter = ('category', 'date', 'user')
    search_fields = ('description', 'user__username', 'category__name')
    readonly_fields = ('created_at',)
    ordering = ('-date', '-created_at')

@admin.register(MonthlyBudgetSummary)
class MonthlyBudgetSummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'total_expenses', 'remaining_amount')
    list_filter = ('month', 'user')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-month', '-created_at')
'''
