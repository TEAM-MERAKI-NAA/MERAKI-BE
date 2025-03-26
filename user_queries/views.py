from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Category, Community, CommunityRequest
from .serializers import CategorySerializer, CommunitySerializer, CommunityRequestSerializer

class CategoryListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class CommunityListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        communities = category.communities.all()
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data)

class CommunityRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommunityRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(requester=request.user)
            return Response({"message": "Your request has been submitted for review."}, status=201)
        return Response(serializer.errors, status=400)
