# rssparser/urls.py
from django.urls import path
from .views import fetch_news, get_news_items,categories,readouts,news_releases, backgrounders, media_advisories, statements, speeches


urlpatterns = [
    path('fetch-store/', fetch_news, name='fetch_news'),
    path('fetch/', get_news_items, name='get_news_items'),
    path('categories/', categories, name='categories'),
    path('categories/readouts/', readouts, name='readouts'),
    path('categories/news-releases/',news_releases, name='news_releases'),
    path('categories/backgrounders/', backgrounders, name='backgrounders'),
    path('categories/media-advisories/', media_advisories, name='media_advisories'),
    path('categories/statements/', statements, name='statements'),
    path('categories/speeches/', speeches, name='speeches'),
 
]
