from rest_framework import serializers
from .models import Guide

class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ('id', 'title', 'description', 'image', 'slug', 'order', 'created_at', 'updated_at')
        lookup_field = 'slug'
