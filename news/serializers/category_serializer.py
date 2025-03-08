from rest_framework import serializers
from ..models.newsletter_category import NewsletterCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterCategory
        fields = ('id', 'title')
