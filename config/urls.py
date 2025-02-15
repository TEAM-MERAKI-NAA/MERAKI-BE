"""Smartwakil URL Configuration"""
from django.contrib import admin
from django.urls import re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.generic.base import TemplateView, RedirectView
from django.views.static import serve
from authentication import views as userviews
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.decorators.cache import cache_control

admin.site.site_header = 'ImmigrationHub'
admin.site.site_title = 'ImmigrationHub'
urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+[

    re_path(r'^admin/', admin.site.urls),
    re_path(r'^admin', admin.site.urls),
    re_path(r'', include('authentication.urls')),
    re_path(r'', include('news.urls')),
    re_path(r'', include('point.urls')),
    re_path(r'', include('guide.urls')),
    re_path('api/password_reset/',
         include('django_rest_passwordreset.urls', namespace='password_reset')),

    re_path('ckeditor5/', include('django_ckeditor_5.urls')),
    re_path(r'^$', TemplateView.as_view(template_name='index.html')),
    re_path(r'^ngsw-worker.js', cache_control(max_age=2592000)(TemplateView.as_view(
        template_name="ngsw-worker.js",
        content_type='application/javascript',
    )), name='ngsw-worker.js'),
    re_path(r'^ngsw.json', RedirectView.as_view(
        url='/static/web/smartwakil/ngsw.json', permanent=False)),
    re_path(r'^(?!/?static/)(?!/?media/)(?P<path>.*\..*)$',
        RedirectView.as_view(url='/static/web/smartwakil/%(path)s', permanent=False)),
    re_path(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
    re_path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # url(r'^$', TemplateView.as_view(template_name='index.html')),
    #authentication urls
    re_path(r'api/token/', view=userviews.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    re_path(r'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
    
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
