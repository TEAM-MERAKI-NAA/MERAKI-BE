from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from ..models.news import News
from ..models.newsletter_category import NewsletterCategory
from ..serializers.news_serializer import NewsCreateSerializer, NewsSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from rest_framework.decorators import permission_classes
from django.db.models import Count


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        limit = int(request.query_params.get('per_page', 10))
        main_category = request.query_params.get('main_category', None)
        category = request.query_params.get('category', None)
        offset = int(request.query_params.get('page', 0))
        queryset = News.objects.all()
        query = Q(status='published')
        
        if main_category:
            query.add(Q(main_categories=main_category), Q.AND)
        
        if category:
            query.add(Q(categories__id=category), Q.AND)
        
        queryset = queryset.filter(query).order_by('-published_date')
        total = len(queryset)

        #for pagination
        offset = offset * limit
        queryset = queryset[offset:offset + limit]
        #for pagination
        #limits
        
        res = NewsSerializer(queryset,many=True).data
        result = {
            'result': res,
            'total': total
        }
        return Response(result)


@permission_classes((AllowAny, ))
class GetCategoriesViewSet(APIView):
    def post(self, request,  format=None):
        main_category = request.data.get('main_category', None)
        query = Q(news__status='published')
        if main_category:
            query.add(Q(news__main_categories=main_category), Q.AND)
        categories = NewsletterCategory.objects.prefetch_related('news').filter(
            query
        ).annotate(total_news = Count('id')).values('id','slug', 'title','total_news')

        if categories:
            return Response({'status': True, 'result': categories})
        return Response({'status': False, 'result': []}, 200)
        # if search:
        #     description = None

        #     # news = News.objects.annotate(
        #     #     search=SearchVector('title') +
        #     #     SearchVector('long_description'),
        #     # ).filter(search__contains=search).distinct()
        #     # query = SearchQuery(search)
        #     news = News.objects.filter(search_vector__icontains=search)
        #     qs = sorted(news,
        #                 key=lambda instance: instance.created_at,
        #                 reverse=True)[:8]
        #     result = []

        #     i = 0
        #     for res in qs:
        #         slug = res.slug
        #         description = res.short_description

        #         result.append({
        #             'title': res.title,
        #             'description': description,
        #             'slug': '/news/details/'+slug,
        #             'created_at': res.created_at
        #         })

        #     return Response({'status': True, 'result': result})
        # return Response({'status': False, 'result': 'No Item Found'}, 200)

class CreateNewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsCreateSerializer

    def list(self, request, *args, **kwargs):
        queryset = News.objects.filter(user=request.user)
        res = NewsCreateSerializer(queryset,many=True).data
        return Response(res)


class NewsChoicesViewSet(APIView):
    def get(self, request, format=None):
        newsFields = News._meta.get_fields()
        choices = {}
        for news in newsFields:
            if news.choices:
                choices[news.attname] = list(news.choices)
        return Response(choices)