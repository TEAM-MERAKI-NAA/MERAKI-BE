from .models import News, NewsCategory
from rest_framework import serializers

class NewsCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewsCategory
        fields = ('id', 'title')


class NewsSerializer(serializers.ModelSerializer):
    readtime = serializers.ReadOnlyField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = News
        fields = ('id', 'user', 'title','short_description', 'long_description',
        'published_date', 'status', 'image', 'categories','slug',
                  'created_at', 'updated_at', 'readtime')
        lookup_field = 'slug'

class NewsCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = News
        fields = ('id', 'user', 'title', 'short_description', 'long_description',
        'published_date', 'status', 'image', 'categories', 'slug',
                  'created_at', 'updated_at')