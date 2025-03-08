from rest_framework import serializers

class NewsItemSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    link = serializers.URLField()
    summary = serializers.CharField()
    updated = serializers.DateTimeField()
    category = serializers.CharField(max_length=100)
    source = serializers.CharField(max_length=100)
