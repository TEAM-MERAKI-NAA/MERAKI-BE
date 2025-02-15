from django.db.models import fields
from ..models.news import News, NewsCategory
from rest_framework import serializers
from django.db import transaction
import json
from ..models.newsletter_category import NewsletterCategory


class NewsCategorySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='news.id')
    article_title = serializers.ReadOnlyField(source='news.title')
    category_title = serializers.ReadOnlyField(source='category.title')
    
    class Meta:
        model = NewsCategory
        fields = ('id',  'article', 'category', 'news_title', 'category_title')


class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer(source="articlecategory_set", many=True, read_only=True, label='Category')
    readtime = serializers.ReadOnlyField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = News
        fields = ('id', 'user', 'title','short_description', 'long_description',
        'published_date', 'status', 'image', 'main_categories', 'categories', 'category','slug',
                  'created_at', 'updated_at', 'readtime')
        lookup_field = 'slug'

    @transaction.atomic
    def create(self, validated_data):
        news = News.objects.create(**validated_data)
        if "category" in self.initial_data:
            category = self.initial_data.get("category")
            for cat in category:
                category_instance = NewsletterCategory.objects.get(pk=cat)
                NewsCategory(category=category_instance, news=news).save()
        news.save()
        return news

class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = NewsletterCategory
        fields = "__all__"

class NewsCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = News
        fields = ('id', 'user', 'title', 'short_description', 'long_description',
        'published_date', 'status', 'image', 'main_categories', 'categories', 'slug',
                  'created_at', 'updated_at')