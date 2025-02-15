from django.db import models
from autoslug import AutoSlugField

class NewsletterCategory(models.Model):
    id = models.AutoField(primary_key=True)
    title=models.CharField(blank=False,max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'

    def __str__(self):
        return self.title

    
