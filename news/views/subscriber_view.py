from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..models.subscriber import Subscriber
from ..serializers.subscriber_serializer import SubscriberSerializer
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail

#for mailchimp integration
from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError


# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID

# Subscription Logic
def subscribe(email):
    
    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))


@permission_classes((AllowAny, ))
class SubscriberiewSet(APIView):
    def post(self, request,  format=None):
        email = request.data.get('email', None)

        if email:
            try:
                Subscriber.objects.create(
                    email = email
                )
                subscribe(email)
                # send_mail(
                #     'Successfully subscribed',
                #     'You have been successfully subscribed to our newsletter',
                #     'manoj.vattarai@gmail.com',
                #     [email],
                #     fail_silently=False,
                # )

            except Exception as e:
                return Response({'status': False}, 201)

        else:
            return Response({'status': False}, 201)
        return Response({'status': True}, 201)
       
