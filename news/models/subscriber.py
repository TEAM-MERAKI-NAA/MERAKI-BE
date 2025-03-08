from django.db import models
from .newsletter_category import NewsletterCategory

class Subscriber(models.Model):
    first_name=models.CharField(max_length=50,blank=True)
    last_name=models.CharField(max_length=50,blank=True)
    email=models.EmailField(unique=True)
    phone_number=models.CharField(max_length=10,blank=True)
    address=models.CharField(max_length=50,blank=True)
    categories = models.ManyToManyField(NewsletterCategory, related_name='subscriber', through="SubscriberCategory")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email

class SubscriberCategory(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    category = models.ForeignKey(NewsletterCategory, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.subscriber.email + " " + self.category.title