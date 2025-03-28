from django.urls import path
from .views import (
    CategoryListAPIView, 
    CommunityListAPIView, 
    CommunityRequestAPIView, 
    CommunityListByCategoryAPIView,
    ApproveRequestAPIView,
    JoinCommunityAPIView,
    CreatePostAPIView,
    CreateCommentAPIView,
    UpvotePostAPIView, 
    DownvotePostAPIView, 
    UpvoteCommentAPIView,
    DownvoteCommentAPIView,
    PostListAPIView,
    PostDetailAPIView,
    CommentListAPIView,
    SearchAPIView,
    ReportContentAPIView
)

urlpatterns = [
    # List all categories
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    
    # List communities filtered by category ID (if provided)
    path('communities/<int:category_id>/', CommunityListAPIView.as_view(), name='community-list-by-id'),
    
    # List/Filter communities by query parameter (category name)
    path('communities/', CommunityListByCategoryAPIView.as_view(), name='community-list-by-category'),

    # Community requests and membership endpoints
    path('communities/request/', CommunityRequestAPIView.as_view(), name='community-request'),
    path('communities/<int:community_id>/join/', JoinCommunityAPIView.as_view(), name='join-community'),
    path('communities/requests/<int:request_id>/approve/', ApproveRequestAPIView.as_view(), name='approve-request'),

    # Posts endpoints
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('posts/<int:post_id>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('communities/<int:community_id>/posts/', PostListAPIView.as_view(), name='community-posts'),
    path('posts/<int:post_id>/upvote/', UpvotePostAPIView.as_view(), name='upvote-post'),
    path('posts/<int:post_id>/downvote/', DownvotePostAPIView.as_view(), name='downvote-post'),

    # Comments endpoints
    path('posts/<int:post_id>/comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('posts/<int:post_id>/comments/create/', CreateCommentAPIView.as_view(), name='create-comment'),
    path('comments/<int:comment_id>/upvote/', UpvoteCommentAPIView.as_view(), name='upvote-comment'),
    path('comments/<int:comment_id>/downvote/', DownvoteCommentAPIView.as_view(), name='downvote-comment'),

    # Search and reporting endpoints
    path('search/', SearchAPIView.as_view(), name='search'),
    path('report/<str:content_type>/<int:content_id>/', ReportContentAPIView.as_view(), name='report-content'),
]
