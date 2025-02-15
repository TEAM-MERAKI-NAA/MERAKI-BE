# rssparser/urls.py
from django.urls import path
from .views import fetch_news
from .views import fetch_news, get_news_items

urlpatterns = [
    path('fetch-from-api/', fetch_news, name='fetch_news'),
    path('fetch-from-db/', get_news_items, name='get_news_items')
]
