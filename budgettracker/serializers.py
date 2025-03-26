from rest_framework import serializers
from .models import Income, ExpenseCategory, Expense, BudgetRecommendation, FinancialSummary

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