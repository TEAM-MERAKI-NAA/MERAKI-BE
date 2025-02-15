from django.db import models

class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()
    summary = models.TextField()
    updated = models.DateTimeField()
    category = models.CharField(max_length=100)
    source = models.CharField(max_length=100)

    def __str__(self):
        return self.title
