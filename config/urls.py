"""
URL configuration for immigrationhub project.

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
from django.urls import path
from django.urls.conf import include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView, RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

admin.site.site_header = 'ImmigrationHub'
admin.site.site_title = 'ImmigrationHub'

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('news/', include('news.urls')),
    path('guide/', include('guide.urls')),
    path('rssparser/', include('rssparser.urls')),
    path('currencyrates/', include('currencyrates.urls')),
    re_path(r'^$', TemplateView.as_view(template_name='index.html')),
    re_path(r'^(?!/?static/)(?!/?media/)(?P<path>.*\..*)$', RedirectView.as_view(url='/static/web/immigrationhub/%(path)s', permanent=False)),
    re_path('ckeditor/', include('ckeditor_uploader.urls')),
    re_path('ckeditor5/', include('django_ckeditor_5.urls')),
    re_path(r'api/schema/', SpectacularAPIView.as_view(), name='schema'),
    re_path(r'api/explorer', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    re_path(r'api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
