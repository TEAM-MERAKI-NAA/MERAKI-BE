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
    description = CKEditor5Field(config_name='extends', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('order',)