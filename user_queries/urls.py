from django.urls import path
from .views import CategoryListAPIView, CommunityListAPIView, CommunityRequestAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:category_id>/communities/', CommunityListAPIView.as_view(), name='community-list'),
    path('communities/request/', CommunityRequestAPIView.as_view(), name='community-request'),
]
