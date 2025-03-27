from django.urls import path
from .views import (
    CategoryListAPIView, 
    CommunityListAPIView, 
    CommunityRequestAPIView, 
    CommunityListByCategoryAPIView,ApproveRequestAPIView,
    JoinCommunityAPIView,CreateCommentAPIView,UpvotePostAPIView, DownvotePostAPIView, UpvoteCommentAPIView,DownvoteCommentAPIView 
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
    path('communities/<int:community_id>/join/', JoinCommunityAPIView.as_view(), name='join-community'),
    path('communities/requests/<int:request_id>/approve/', ApproveRequestAPIView.as_view(), name='approve-request'),
    path('api/posts/<int:post_id>/comments/', CreateCommentAPIView.as_view(), name='create-comment'),

    # Upvote or downvote a post
    path('posts/<int:post_id>/upvote/', UpvotePostAPIView.as_view(), name='upvote-post'),
    path('posts/<int:post_id>/downvote/', DownvotePostAPIView.as_view(), name='downvote-post'),

    # Upvote or downvote a comment
    path('comments/<int:comment_id>/upvote/', UpvoteCommentAPIView.as_view(), name='upvote-comment'),
    path('comments/<int:comment_id>/downvote/', DownvoteCommentAPIView.as_view(), name='downvote-comment'),
]
