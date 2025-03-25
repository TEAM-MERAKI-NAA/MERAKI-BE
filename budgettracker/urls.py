from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'incomes', views.IncomeViewSet, basename='income')
router.register(r'expense-categories', views.ExpenseCategoryViewSet, basename='expense-category')
router.register(r'expenses', views.ExpenseViewSet, basename='expense')
router.register(r'budget-recommendations', views.BudgetRecommendationViewSet, basename='budget-recommendation')
router.register(r'financial-summaries', views.FinancialSummaryViewSet, basename='financial-summary')

app_name = 'budgettracker'

urlpatterns = [
    path('api/', include(router.urls)),
    # Additional API endpoints
    path('api/current-month-summary/', views.CurrentMonthSummaryView.as_view(), name='current-month-summary'),
    path('api/spending-by-category/', views.SpendingByCategoryView.as_view(), name='spending-by-category'),
    path('api/monthly-trends/', views.MonthlyTrendsView.as_view(), name='monthly-trends'),
    path('api/recommendations/', views.BudgetRecommendationsView.as_view(), name='budget-recommendations'),
] 