from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'budget', views.BudgetViewSet, basename='budget')

app_name = 'budgettracker'

urlpatterns = [
    path('api/', include(router.urls)),
] 