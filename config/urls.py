"""
URL configuration for ImmigrationHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.generic.base import TemplateView
from django.views.static import serve
from authentication import views as userviews
from rest_framework_simplejwt.views import TokenRefreshView

admin.site.site_header = 'ImmigrationHub'
admin.site.site_title = 'ImmigrationHub'
urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+[

    re_path(r'^admin', admin.site.urls),
    path(r'api/authentication', include('authentication.urls')),

    re_path(r'^$', TemplateView.as_view(template_name='index.html')),


    re_path(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),

    #authentication urls
    path(r'api/token/', view=userviews.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path(r'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)