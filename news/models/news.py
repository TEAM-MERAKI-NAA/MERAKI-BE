from __future__ import unicode_literals
from django.db import models
from .newsletter_category import NewsletterCategory
from django.conf import settings
from autoslug import AutoSlugField
from datetime import datetime
import readtime
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django_ckeditor_5.fields import CKEditor5Field


class News(models.Model):

    STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )


    CATEGORIES = (
        ('guides', 'Guides'),
        ('updates', 'Updates'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(blank=False, max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True)
    short_description = models.TextField(blank=False)
    long_description = CKEditor5Field(config_name='extends', blank=False)
    published_date = models.DateField(null=True)

    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    image = models.ImageField(upload_to='news/')

    main_categories = models.CharField(max_length=20, choices=CATEGORIES)
    categories = models.ManyToManyField(
        NewsletterCategory, related_name='news', through="NewsCategory", verbose_name='Categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    search_vector = SearchVectorField(null=True)

    def __init__(self, *args, **kwargs):
        super(News, self).__init__(*args, **kwargs)
        self.old_status = self.status

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == 'published' and self.old_status != self.status:
            self.published_date = datetime.now()
        if self.status != 'published' and self.old_status != self.status:
            self.published_date = None

        image = Image.open(self.image)
        fixed_height = image.size[1]
        if fixed_height > 1200:
            fixed_height = 1200
        height_percent = (fixed_height / float(image.size[1]))

        width_size = int((float(image.size[0]) * float(height_percent)))
        image = image.resize((width_size, fixed_height), Image.NEAREST)
        image_format = image.format
        formatt = 'PNG'
        extension = 'png'
        tt = 'image/png'
        if image_format == 'JPEG':
            formatt = 'JPEG'
            extension = 'jpg'
            tt = 'image/jpeg'
        imagename = "{}.{}".format(self.image.name.split('.')[0], extension)
        output = BytesIO()
        image.save(output, format=formatt, quality=100, optimize=True)
        output.seek(0)
        self.image = InMemoryUploadedFile(output, 'ImageField', imagename, tt,
                                          sys.getsizeof(output), None)
        super(News, self).save(*args, **kwargs)


    def readtime(self):
        result = readtime.of_text(self.long_description)
        return result.text

    class Meta:
        indexes = (GinIndex(fields=["search_vector"]),)  # add index
        ordering = ('-created_at',)


class NewsCategory(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    category = models.ForeignKey(NewsletterCategory, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.news.title + " " + self.category.title
