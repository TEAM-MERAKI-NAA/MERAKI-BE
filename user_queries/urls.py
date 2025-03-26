from django.urls import path
from .views import (
    CategoryListAPIView, 
    CommunityListAPIView, 
    CommunityRequestAPIView, 
    CommunityListByCategoryAPIView
)

urlpatterns = [
    # List all categories
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    
    # List all communities, optionally filter by category ID
    path('communities/<int:category_id>/', CommunityListAPIView.as_view(), name='community-list-by-id'),
    
    # Filter communities by category name (query param)
    path('communities/', CommunityListByCategoryAPIView.as_view(), name='community-list-by-category'),

    # Submit community requests
    path('communities/request/', CommunityRequestAPIView.as_view(), name='community-request'),
]
