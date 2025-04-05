from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import GuideSerializer
from .models import Guide
from rest_framework.permissions import AllowAny


# Create your views here.

class GuideViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
    permission_classes = [AllowAny,]
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        queryset = Guide.objects.filter(status="active")
        res = GuideSerializer(queryset,many=True).data
        return Response(res)