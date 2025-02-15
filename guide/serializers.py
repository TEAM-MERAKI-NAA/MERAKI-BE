from rest_framework import serializers
from .models import Guide, SubGuide

class SubGuideSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubGuide
        fields = ('id', 'title', 'description')

class GuideSerializer(serializers.ModelSerializer):
    subguides = SubGuideSerializer(many=True, read_only=True)

    class Meta:
        model = Guide
        fields = ('id', 'title', 'short_description', 'image', 'slug', 'subguides', 'order', 'created_at', 'updated_at')
        lookup_field = 'slug'
