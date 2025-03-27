from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Category, Community, CommunityRequest
from .utils import approve_request
from .serializers import CategorySerializer, CommunitySerializer, CommunityRequestSerializer


class BaseAPIView(APIView):
    """
    A base class for shared functionality or settings, if needed.
    This simplifies code duplication.
    """
    pass


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
