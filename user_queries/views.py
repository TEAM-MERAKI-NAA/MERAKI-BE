from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Community, CommunityRequest
from .serializers import CommunitySerializer, CommunityRequestSerializer

class CommunityListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        communities = Community.objects.all()
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data)

class JoinCommunityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, community_id):
        community = get_object_or_404(Community, id=community_id)
        community.members.add(request.user)
        return Response({"message": f"You have joined {community.name}"})

class CommunityRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommunityRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(requester=request.user)
            return Response({"message": "Your community request has been submitted for review."})
        return Response(serializer.errors, status=400)
