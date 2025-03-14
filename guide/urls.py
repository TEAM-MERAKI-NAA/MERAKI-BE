from django.urls import path, include
from rest_framework import routers
from .views import GuideViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'guides', GuideViewSet)
urlpatterns = [
    path(r'api/', include(router.urls)),
]
