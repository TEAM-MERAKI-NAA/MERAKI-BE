from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q
from .models import News
from .serializers import NewsCreateSerializer, NewsSerializer
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import News, NewsCategory
from .serializers import NewsSerializer, NewsCreateSerializer, NewsCategorySerializer


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        limit = int(request.query_params.get('per_page', 10))
        category = request.query_params.get('categories', None)
        category = request.query_params.get('category', None)
        offset = int(request.query_params.get('page', 0))
        queryset = News.objects.all()
        query = Q(status='published')
        
        if category:
            query.add(Q(categories=category), Q.AND)
        
        if category:
            query.add(Q(categories__id=category), Q.AND)
        
        queryset = queryset.filter(query).order_by('-published_date')
        total = len(queryset)

        #for pagination
        offset = offset * limit
        queryset = queryset[offset:offset + limit]
        
        res = NewsSerializer(queryset,many=True).data
        result = {
            'result': res,
            'total': total
        }
        return Response(result)

class CreateNewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsCreateSerializer

    def list(self, request, *args, **kwargs):
        queryset = News.objects.filter(user=request.user)
        res = NewsCreateSerializer(queryset,many=True).data
        return Response(res)
    

class NewsCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer
    permission_classes = [AllowAny]