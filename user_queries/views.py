from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.cache import cache
from .models import Category, Community, CommunityRequest, Post, Comment
from .utils import approve_request
from .serializers import (
    CategorySerializer, CommunitySerializer, CommunityRequestSerializer,
    PostSerializer, CommentSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class BaseAPIView(APIView):
    pagination_class = StandardResultsSetPagination

    def get_paginated_response(self, data):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(data, self.request)
        return paginator.get_paginated_response(result_page)


class CategoryListAPIView(BaseAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Fetch and serialize all categories
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CommunityListAPIView(BaseAPIView):
    permission_classes = [AllowAny]

    def get(self, request, category_id=None):
        # Fetch communities filtered by category ID if provided
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            communities = category.communities.all()
        else:
            communities = Community.objects.all()
        
        # Serialize and return community data
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data)


class CommunityListByCategoryAPIView(BaseAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Get category name from query parameters
        category_name = request.query_params.get('category', None)

        if category_name:
            # Fetch category by name (case-insensitive) and its communities
            category = get_object_or_404(Category, name__iexact=category_name)
            communities = category.communities.all()
        else:
            # If no category is provided, fetch all communities
            communities = Community.objects.all()
        
        # Serialize and return community data
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data)


class CommunityRequestAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Validate and save community request
        serializer = CommunityRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(requester=request.user)
            return Response(
                {"message": "Your request has been submitted for review."}, 
                status=201
            )
        return Response(serializer.errors, status=400)


class ApproveRequestAPIView(APIView):
    def post(self, request, request_id):
        # Approve the request and handle any potential exceptions
        try:
            approve_request(request_id)
            return Response({"message": "Community request approved and community created!"}, status=200)
        except CommunityRequest.DoesNotExist:
            return Response({"error": "Request not found or already approved."}, status=404)

class JoinCommunityAPIView(APIView):
    permission_classes = [AllowAny]  # Can be changed to IsAuthenticated later

    def post(self, request, community_id):
        community = get_object_or_404(Community, id=community_id)
        community.members_count += 1
        community.save()
        return Response({
            "message": f"You've successfully joined the {community.name} community!",
            "members_count": community.members_count
        }, status=200)

class CreatePostAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, community_id):
        community = get_object_or_404(Community, id=community_id)
        if not CommunityMembership.objects.filter(user=request.user, community=community).exists():
            return Response({"error": "You must join this community to post."}, status=403)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, community=community)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class CreateCommentAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        community = post.community
        if not CommunityMembership.objects.filter(user=request.user, community=community).exists():
            return Response({"error": "You must join this community to comment."}, status=403)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UpvotePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.upvotes += 1
        post.save()
        return Response({"upvotes": post.upvotes}, status=200)

class DownvotePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.downvotes += 1
        post.save()
        return Response({"downvotes": post.downvotes}, status=200)

class UpvoteCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.upvotes += 1
        comment.save()
        return Response({"upvotes": comment.upvotes}, status=200)

class DownvoteCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.downvotes += 1
        comment.save()
        return Response({"downvotes": comment.downvotes}, status=200)

class PostListAPIView(BaseAPIView):
    permission_classes = [AllowAny]

    def get(self, request, community_id=None):
        # Get sorting parameter
        sort_by = request.query_params.get('sort', 'new')
        
        # Base queryset
        posts = Post.objects.all()
        
        if community_id:
            posts = posts.filter(community_id=community_id)
        
        # Apply sorting
        if sort_by == 'hot':
            posts = posts.order_by('-upvotes', '-created_at')
        elif sort_by == 'top':
            posts = posts.order_by('-upvotes')
        elif sort_by == 'new':
            posts = posts.order_by('-created_at')
        elif sort_by == 'controversial':
            posts = posts.order_by('-downvotes')
        
        # Cache key
        cache_key = f'posts_{community_id}_{sort_by}_{request.query_params.get("page", 1)}'
        
        # Try to get from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        # Serialize and paginate
        serializer = PostSerializer(posts, many=True)
        response_data = self.get_paginated_response(serializer.data)
        
        # Cache for 5 minutes
        cache.set(cache_key, response_data, 300)
        
        return response_data

class PostDetailAPIView(BaseAPIView):
    permission_classes = [AllowAny]

    def get(self, request, post_id):
        post = get_object_or_404(Post.objects.select_related('author', 'community'), id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

class CommentListAPIView(BaseAPIView):
    permission_classes = [AllowAny]

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post).select_related('author')
        
        # Get sorting parameter
        sort_by = request.query_params.get('sort', 'new')
        
        if sort_by == 'top':
            comments = comments.order_by('-upvotes')
        elif sort_by == 'new':
            comments = comments.order_by('-created_at')
        elif sort_by == 'controversial':
            comments = comments.order_by('-downvotes')
        
        serializer = CommentSerializer(comments, many=True)
        return self.get_paginated_response(serializer.data)

class SearchAPIView(BaseAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '')
        search_type = request.query_params.get('type', 'all')
        
        if not query:
            return Response({"error": "Search query is required"}, status=400)
        
        results = {}
        
        if search_type in ['all', 'communities']:
            communities = Community.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query)
            )
            results['communities'] = CommunitySerializer(communities, many=True).data
        
        if search_type in ['all', 'posts']:
            posts = Post.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            ).select_related('author', 'community')
            results['posts'] = PostSerializer(posts, many=True).data
        
        return Response(results)

class ReportContentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, content_type, content_id):
        if content_type not in ['post', 'comment']:
            return Response({"error": "Invalid content type"}, status=400)
        
        reason = request.data.get('reason')
        if not reason:
            return Response({"error": "Reason is required"}, status=400)
        
        # Here you would typically create a Report model instance
        # For now, we'll just return success
        return Response({"message": "Content reported successfully"}, status=200)
