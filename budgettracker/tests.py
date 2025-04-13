# from django.test import TestCase
# from django.urls import reverse
# from rest_framework.test import APITestCase, APIClient
# from rest_framework import status
# from django.contrib.auth import get_user_model
# from decimal import Decimal
# from .models import UserMonthlyBudget, BudgetCategory, BudgetExpense, MonthlyBudgetSummary
# from django.utils import timezone

# User = get_user_model()

# class BudgetTrackerAPITests(APITestCase):
#     def setUp(self):
#         # Create test user
#         self.user = User.objects.create_user(
#             username='testuser',
#             email='test@example.com',
#             password='testpass123'
#         )
        
#         # Create client and authenticate
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
        
#         # Create test data
#         self.monthly_budget = UserMonthlyBudget.objects.create(
#             user=self.user,
#             monthly_income=Decimal('5000.00')
#         )
        
#         self.category = BudgetCategory.objects.create(
#             user=self.user,
#             name='Food',
#             is_fixed=True
#         )

#     def test_create_monthly_budget(self):
#         """Test creating a monthly budget"""
#         url = reverse('budgettracker:monthly-budget-list')
#         data = {
#             'monthly_income': '5000.00'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(UserMonthlyBudget.objects.count(), 2)  # Including the one from setUp

#     def test_create_budget_category(self):
#         """Test creating a budget category"""
#         url = reverse('budgettracker:budget-category-list')
#         data = {
#             'name': 'Transportation',
#             'is_fixed': True
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(BudgetCategory.objects.count(), 2)  # Including the one from setUp

#     def test_create_budget_expense(self):
#         """Test creating a budget expense"""
#         url = reverse('budgettracker:budget-expense-list')
#         data = {
#             'category': self.category.id,
#             'amount': '100.00',
#             'description': 'Grocery shopping',
#             'date': timezone.now().date().isoformat()
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(BudgetExpense.objects.count(), 1)

#     def test_get_monthly_summary(self):
#         """Test getting monthly summary"""
#         # Create an expense first
#         BudgetExpense.objects.create(
#             user=self.user,
#             category=self.category,
#             amount=Decimal('100.00'),
#             description='Test expense',
#             date=timezone.now()
#         )

#         url = reverse('budgettracker:monthly-summary-current_month')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['total_expenses'], '100.00')
#         self.assertEqual(response.data['remaining_amount'], '4900.00')

#     def test_list_budget_categories(self):
#         """Test listing budget categories"""
#         url = reverse('budgettracker:budget-category-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)  # Only the one from setUp

#     def test_list_budget_expenses(self):
#         """Test listing budget expenses"""
#         # Create a test expense
#         BudgetExpense.objects.create(
#             user=self.user,
#             category=self.category,
#             amount=Decimal('100.00'),
#             description='Test expense',
#             date=timezone.now()
#         )

#         url = reverse('budgettracker:budget-expense-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

#     def test_update_monthly_budget(self):
#         """Test updating monthly budget"""
#         url = reverse('budgettracker:monthly-budget-detail', args=[self.monthly_budget.id])
#         data = {
#             'monthly_income': '6000.00'
#         }
#         response = self.client.patch(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.monthly_budget.refresh_from_db()
#         self.assertEqual(self.monthly_budget.monthly_income, Decimal('6000.00'))

#     def test_delete_budget_expense(self):
#         """Test deleting a budget expense"""
#         expense = BudgetExpense.objects.create(
#             user=self.user,
#             category=self.category,
#             amount=Decimal('100.00'),
#             description='Test expense',
#             date=timezone.now()
#         )

#         url = reverse('budgettracker:budget-expense-detail', args=[expense.id])
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(BudgetExpense.objects.count(), 0)

#     def test_unauthorized_access(self):
#         """Test unauthorized access to endpoints"""
#         # Create a new client without authentication
#         unauthorized_client = APIClient()
        
#         # Try to access various endpoints
#         urls = [
#             reverse('budgettracker:monthly-budget-list'),
#             reverse('budgettracker:budget-category-list'),
#             reverse('budgettracker:budget-expense-list'),
#             reverse('budgettracker:monthly-summary-current_month')
#         ]
        
#         for url in urls:
#             response = unauthorized_client.get(url)
#             self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
