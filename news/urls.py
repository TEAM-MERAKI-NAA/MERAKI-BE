from django.urls import path, include
from rest_framework import routers
from .views import NewsViewSet, NewsCategoryViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'list', NewsViewSet)
router.register(r'category_list', NewsCategoryViewSet)

urlpatterns = [
    path(r'api/', include(router.urls)),
]
