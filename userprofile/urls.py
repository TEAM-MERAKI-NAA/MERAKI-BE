from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profile', views.UserProfileViewSet, basename='profile')

app_name = 'userprofile'

urlpatterns = [
    path('api/', include(router.urls)),
    path('profile/', views.profile_view, name='profile_view'),
] 