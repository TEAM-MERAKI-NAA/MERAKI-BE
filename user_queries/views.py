from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Category, Community, CommunityRequest
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
