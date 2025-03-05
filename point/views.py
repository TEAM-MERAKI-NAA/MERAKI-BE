from .serializers import PointSerializer
from .models import Point
from rest_framework import viewsets
from rest_framework.response import Response


# Create your views here.

class PointViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = Point.objects.filter(user=request.user)
        res = PointSerializer(queryset,many=True).data
        return Response(res)
