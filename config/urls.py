"""ImmigrationHub URL Configuration"""
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
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

admin.site.site_header = 'ImmigrationHub'
admin.site.site_title = 'ImmigrationHub'
urlpatterns = [

    re_path(r'^admin/', admin.site.urls),
    re_path(r'^admin', admin.site.urls),
    re_path(r'auth/', include('authentication.urls')),
    re_path(r'news/', include('news.urls')),
    re_path(r'point/', include('point.urls')),
    re_path(r'guide/', include('guide.urls')),
    re_path(r'currencyrates/', include('currencyrates.urls')),
    re_path(r'profile/', include('my_profile.urls')),
    re_path(r'rssparser/', include('rssparser.urls')),
    re_path('api/password_reset/',
         include('django_rest_passwordreset.urls', namespace='password_reset')),

    re_path('ckeditor5/', include('django_ckeditor_5.urls')),
    re_path(r'^$', TemplateView.as_view(template_name='index.html')),
    re_path(r'^ngsw-worker.js', cache_control(max_age=2592000)(TemplateView.as_view(
        template_name="ngsw-worker.js",
        content_type='application/javascript',
    )), name='ngsw-worker.js'),
    re_path(r'^ngsw.json', RedirectView.as_view(
        url='/static/web/immigrationhub/ngsw.json', permanent=False)),
    re_path(r'^(?!/?static/)(?!/?media/)(?P<path>.*\..*)$',
        RedirectView.as_view(url='/static/web/immigrationhub/%(path)s', permanent=False)),
    re_path(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
    re_path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # url(r'^$', TemplateView.as_view(template_name='index.html')),
    #authentication urls
    re_path(r'api/token/', view=userviews.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    re_path(r'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   

    re_path('api/', include('rssparser.urls')),
    re_path('api/', include('currencyrates.urls')),
    # Full-fledged API Explorer
    re_path(r'api/schema/', SpectacularAPIView.as_view(), name='schema'),
    re_path(r'api/explorer', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    re_path(r'api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    
]
if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
