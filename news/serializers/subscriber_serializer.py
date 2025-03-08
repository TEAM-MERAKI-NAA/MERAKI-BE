from ..models.subscriber import Subscriber, SubscriberCategory
from rest_framework import serializers
from django.db import transaction
import json
from ..models.newsletter_category import NewsletterCategory


class SubscriberCategorySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='subscriber.id')
    subscriber_title = serializers.ReadOnlyField(source='subscriber.title')
    category_title = serializers.ReadOnlyField(source='category.title')
    
    class Meta:
        model = SubscriberCategory
        fields = ('id',  'subscriber', 'category', 'subscriber_title', 'category_title')


class SubscriberSerializer(serializers.ModelSerializer):
    category = SubscriberCategorySerializer(source="subscribercategory_set", many=True, read_only=True)

    class Meta:
        model = Subscriber
        fields = ('id', 'email',
        'created_at', 'updated_at')

    @transaction.atomic
    def create(self, validated_data):
        subscriber = Subscriber.objects.create(**validated_data)
        if "category" in self.initial_data:
            category = self.initial_data.get("category")
            for cat in category:
                category_instance = NewsletterCategory.objects.get(pk=cat)
                SubscriberCategory(category=category_instance, subscriber=subscriber).save()
        subscriber.save()
        return subscriber

