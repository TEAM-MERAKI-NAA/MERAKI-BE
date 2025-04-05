from rest_framework import serializers
from .models import Budget

class BudgetSerializer(serializers.ModelSerializer):
    remaining_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Budget
        fields = ['id', 'monthly_income', 'category', 'amount', 'description', 'date', 'remaining_amount', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

# Commented out other serializers
'''
class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'user', 'amount', 'frequency', 'description', 'date', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'user', 'category', 'category_name', 'amount', 'description', 'date', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class BudgetRecommendationSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = BudgetRecommendation
        fields = ['id', 'category', 'category_name', 'tip_title', 'description', 'local_discount_info', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class FinancialSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialSummary
        fields = ['id', 'user', 'start_date', 'end_date', 'total_income', 'total_expenses', 'remaining_balance', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, data):
        if data.get('total_income', 0) < 0:
            raise serializers.ValidationError("Total income cannot be negative")
        if data.get('total_expenses', 0) < 0:
            raise serializers.ValidationError("Total expenses cannot be negative")
        return data 

class UserMonthlyBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMonthlyBudget
        fields = ['id', 'monthly_income', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class BudgetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetCategory
        fields = ['id', 'name', 'is_fixed', 'created_at']
        read_only_fields = ['created_at']

class BudgetExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = BudgetExpense
        fields = ['id', 'category', 'category_name', 'amount', 'description', 'date', 'created_at']
        read_only_fields = ['created_at']

class MonthlyBudgetSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBudgetSummary
        fields = ['id', 'month', 'total_expenses', 'remaining_amount', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
''' 