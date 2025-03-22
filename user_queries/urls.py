from django.urls import path
from .views import CommunityListAPIView, JoinCommunityAPIView, CommunityRequestAPIView

urlpatterns = [
    path('communities/', CommunityListAPIView.as_view(), name='community-list'),
    path('communities/<int:community_id>/join/', JoinCommunityAPIView.as_view(), name='join-community'),
    path('communities/request/', CommunityRequestAPIView.as_view(), name='community-request'),
]
