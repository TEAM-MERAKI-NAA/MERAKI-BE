from rest_framework import viewsets
from rest_framework.response import Response
from ..models.news import News
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.db.models import F

@permission_classes((AllowAny, ))
class SearchViewSet(APIView):
    def post(self, request,  format=None):
        search = request.data.get('s', None)

        if search:
            description = None
            
            # article = News.objects.annotate(
            #     search=SearchVector('title') +
            #     SearchVector('long_description'),
            # ).filter(search__contains=search).distinct()
            # query = SearchQuery(search)
            article = News.objects.filter(search_vector__icontains=search)
            qs = sorted(article,
                        key=lambda instance: instance.created_at, 
                        reverse=True)[:8]
            result = []
           
            i = 0
            for res in qs:
                slug = res.slug
                description = res.short_description
               
                result.append({
                    'title': res.title,
                    'description': description,
                    'slug': '/article/details/'+slug,
                    'created_at': res.created_at
                })

            return Response({'status': True, 'result': result})
        return Response({'status': False, 'result': 'No Item Found'}, 200)
