from .views.category_view import NewsCategoryViewSet
from django.urls import path, include
from rest_framework import routers
from .views.news_view import GetCategoriesViewSet, NewsChoicesViewSet, NewsViewSet
from .views.subscriber_view import SubscriberiewSet
from .views.feed import LatestPostsFeed
from .views.search_view import SearchViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'news', NewsViewSet)
router.register(r'category_news', NewsCategoryViewSet)
urlpatterns = [
    path(r'api/', include(router.urls)),
    path('api/subscribe-newsletter', SubscriberiewSet.as_view(), name="subscribe"),
    path('api/news-search', SearchViewSet.as_view(), name='allsearchresult'),
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path('api/news_filter', GetCategoriesViewSet.as_view(), name='article_filter'),
    path('api/news_choices', NewsChoicesViewSet.as_view(), name='news_choice'),
]
