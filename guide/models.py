from autoslug.fields import AutoSlugField
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Guide(models.Model):
    STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=STATUS, default='inactive')
    image = models.ImageField(upload_to = 'guides/', blank=True, null = True)
    short_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('order',)

class SubGuide(models.Model):
    title = models.CharField(max_length=200)
    description = CKEditor5Field(config_name='extends')
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='subguides')
    order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('order',)