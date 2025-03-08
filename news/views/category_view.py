from rest_framework import viewsets
from ..models.newsletter_category import NewsletterCategory
from ..serializers.news_serializer import CategorySerializers
from rest_framework.permissions import AllowAny

class NewsCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsletterCategory.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [AllowAny]