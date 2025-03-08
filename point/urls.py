from django.urls import path, include
from rest_framework import routers
from .views import PointViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'my-points', PointViewSet)

urlpatterns = [
    path(r'api/', include(router.urls)),
]