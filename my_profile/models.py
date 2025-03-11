from __future__ import unicode_literals
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db.models.signals import post_save


class MyProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='myprofile', primary_key=True)
    image=models.ImageField(upload_to='profile/', null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    status_in_canada = models.CharField(max_length=20, blank=True, null=True)
    describe_you = models.TextField(max_length=500, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('myprofile-details', kwargs={'pk': self.pk})
   
    def __str__(self):
        if self.first_name:
            return f'{self.first_name} {self.last_name}'
        return (f"{str(self.user)}")

@receiver(post_delete, sender=MyProfile)
def delete_user_signal(sender, instance, **kwargs):
    instance.user.delete()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        MyProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.myprofile.save()
    
