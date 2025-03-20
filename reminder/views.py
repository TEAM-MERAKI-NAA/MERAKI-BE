from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Reminder
from .serializers import ReminderSerializer
from datetime import datetime

# Create your views here.
class ReminderViewSet(viewsets.ModelViewSet):
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def send_reminder(self, request, pk=None):
        reminder = self.get_object()
        if reminder.should_send_reminder():
            subject = f'Reminder: {reminder.title}'
            message = f'''
            This is a reminder for: {reminder.title}
            Document Expiry Date: {reminder.document_expiry_date}
            Frequency: {reminder.frequency}
            '''
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [reminder.user.email],
                    fail_silently=False,
                )
                reminder.last_reminder_sent = timezone.now()
                reminder.save()
                return Response({'status': 'reminder sent'})
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response({'status': 'reminder not due yet'})
