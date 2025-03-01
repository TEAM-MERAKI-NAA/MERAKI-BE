from django.db import models
from django.conf import settings

class AllocatedPoint(models.Model):
    CHOICES= [
        ('registration','On Registration'),
        ('question','On Question Approve'),
        ('answer','On Answer Approve')
        ]
    OPTIONS= [
        ('active','active'),
        ('inactive','inactive')
        ]
        
    title=models.CharField(max_length=20, choices=CHOICES, unique=True)
    allocated_point = models.IntegerField(default=15)
    status = models.CharField(max_length=20, choices=OPTIONS, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = "Allocated Points"
        verbose_name = "Allocated Points"


class Point(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='points')
    points_title=models.ForeignKey(AllocatedPoint, on_delete=models.SET_NULL, null=True)
    title=models.CharField(max_length=100, blank=True, null=True)
    points_earned= models.IntegerField(default=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = "Points"
        verbose_name = "Point"
        ordering = ["-created_at",]

        