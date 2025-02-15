from rest_framework.response import Response
from rest_framework import viewsets
from authentication.models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import UserManagerSerializer, UserSignupSerializer
from .serializers import ChangePasswordSerializer
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
import math
import random
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.core.mail import send_mail
from django.db import transaction
import django.contrib.auth.password_validation as validators
from django.core import exceptions
import pyotp
from django.core.mail.message import EmailMultiAlternatives
from point.models import Point, AllocatedPoint



#for recaptcha
import urllib
import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

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


class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@permission_classes((AllowAny, ))
class ValidateUsernameEmailCustomer(APIView):
    def post(self, request):
        checkdata = request.data['checkdata']
        reqtype = request.data['type']
        status = False
        msg = ''
        if reqtype == 'email':
            obj = User.objects.filter(email=checkdata)
            if obj:
                status = True
                msg = 'Email is already Taken.'

        if reqtype == 'username':
            obj = User.objects.filter(username=checkdata)
            if obj:
                status = True
                msg = 'Username is already Taken'

        if reqtype == 'phone_number':
            obj = User.objects.filter(phone_number=checkdata)
            if obj:
                status = True
                msg = 'Phone Number is already Taken'

        return Response(status)


class CheckIfLoggedIn(APIView):
    def get(self, request):
        currentuser = request.user
        serializer = UserManagerSerializer(currentuser)
        serializerdata = serializer.data
        return Response(serializerdata)


@permission_classes((AllowAny, ))
class UserCreateViewSet(APIView):
    @transaction.atomic
    def post(self, request,  format=None):
        errors = dict()
        try:
            validators.validate_password(request.data['password'])
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        captcha = request.data['captcha']
        request.data.pop('captcha')
        captcharesult = self.checkcaptcha(captcha)
        if captcharesult:
            serialized = UserSignupSerializer(data=request.data)
            
            if serialized.is_valid():
                key = generateKey.returnValue()
                user = User.objects.create(
                    username=request.data['username'],
                    email=request.data['email'],
                    phone_number=request.data['phone_number'],
                    is_staff=False,
                    is_superuser=False,
                    is_active=False,
                    user_type=request.data['user_type'],
                    otp=key['OTP'],
                    activation_key=key['totp']
                )
                user.set_password(request.data['password'])
                user.save()
                email = request.data['email']
                emailtext = """<p>Your One Time Password (OTP ) is <span
                            style="font-weight: bolder; font-size: larger; background-color: rgb(230, 233, 236); padding: 4px;">{}</span>
                    </p>
                    <br>
                    <p>This otp is valid for 1 day only.</p>
                    <em>Thank you</em><br />
                    <em>Team <b>Smart Wakil</b></em>""".format(key['OTP'],)

                send_email = send_mail(
                    # title:
                    "One Time Password.",
                    # message:
                    emailtext,
                    # from:
                    settings.EMAIL_HOST_USER,
                    # to:
                    [email],
                    html_message=emailtext
                )
                
                subscribe(email)

                result = {
                    'data': serialized.data,
                    'status': True
                }
                return Response(result, status=status.HTTP_200_OK)
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('ReCaptcha error', status=status.HTTP_400_BAD_REQUEST)

    def generateOTP(self):
        digits = "0123456789"
        OTP = ""
        for i in range(4):
            OTP += digits[math.floor(random.random() * 10)]
        return OTP

    def checkcaptcha(self, captcha):
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': captcha
        }
        data = urllib.parse.urlencode(values).encode("utf-8")
        req = urllib.request.Request(url, data)
        response = urllib.request.urlopen(req)
        result = json.load(response)

        if result['success']:
            return True
        return False


class ValidateOTP(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        otp = request.data.get('otp', False)
        try:
            user = User.objects.get(otp=otp,is_active=False)
            _otp = user.otp
            if int(otp) != int(_otp):
                return Response({"status": False, "details" : "Invalid otp"},status=status.HTTP_202_ACCEPTED)
                # return Response({"status": False, "details" : "Invalid otp"},status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                activation_key = user.activation_key
                totp = pyotp.TOTP(activation_key, interval=86400)
                verify = totp.verify(otp)
                
                if verify:
                    user.is_active = True
                    user.save()
                    regpoint = AllocatedPoint.objects.filter(
                        title = 'registration'
                    ).first()
                    pp= 10
                    if regpoint:
                        pp = regpoint.allocated_point
                    Point.objects.create(
                        points_title = regpoint,
                        title = 'Registration Completed',
                        points_earned = pp,
                        user = user
                    )

                    emailtext = """
                    <h1>Welcome <strong>{}</strong></h1>
                    <p>Your account successfully activated. Now you can access all the feature of this site!!
                    </p>
                    <br>
                    <em>Thank you</em><br />
                    <em>Team <b>Smart Wakil</b></em>""".format(user.username,)

                    send_email = send_mail(
                        # title:
                        "One Time Password.",
                        # message:
                        emailtext,
                        # from:
                        settings.EMAIL_HOST_USER,
                        # to:
                        [user.email],
                        html_message=emailtext
                    )


                    # email_template = render_to_string('signup_otp_success.html',{"username":user.username})    
                    # sign_up = EmailMultiAlternatives(
                    #         "Account successfully activated", 
                    #         "Account successfully activated",
                    #         settings.EMAIL_HOST_USER, 
                    #         [user.email],
                    #     )
                    # sign_up.attach_alternative(email_template, 'text/html')
                    # sign_up.send()



                    return Response({"status":True, "detail" : "Your account has been successfully activated!!"}, status=status.HTTP_202_ACCEPTED)

                else:
                    return Response({"status": False, "detail" : "Given otp is expired!!"}, status=status.HTTP_202_ACCEPTED)
                    # return Response({"status": False, "detail" : "Given otp is expired!!"}, status=status.HTTP_408_REQUEST_TIMEOUT)
        except Exception as e:
            print(e)
            return Response({"status": False, "detail" : "Invalid OTP OR Account has already been activated"}, status=status.HTTP_202_ACCEPTED)
            # return Response({"status": False, "detail" : "Invalid otp OR No any inactive user found for given otp"}, status=status.HTTP_400_BAD_REQUEST)




        # phone = request.data.get('phone_number', False)
        # otp_sent = request.data.get('otp', False)

        # if phone and otp_sent:
        #     old = User.objects.filter(phone_number__iexact=phone)
        #     if old.exists():
        #         old = old.first()
        #         otp = old.otp
        #         if str(otp_sent) == str(otp):
        #             old.is_active = True
        #             old.otp = None
        #             old.save()
        #             return Response({
        #                 'status': True,
        #                 'detail': 'Account has been activated.',
        #             })

        #         else:
        #             return Response({
        #                 'status': False,
        #                 'detail': 'OTP incorrect.',
        #                 'err_code':  1                    })
        #     else:
        #         return Response({
        #             'status': False,
        #             'detail': 'First proceed via Registration.',
        #             'err_code':  2
        #         })
        # else:
        #     return Response({
        #         'status': False,
        #         'detail': 'Please provide both phone and otp for validations',
        #         'err_code':  3
        #     })


class ResendOTP(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone_number', False)
        if phone:
            old = User.objects.filter(phone_number__iexact=phone)
            
            if old.exists():
                old = old.first()
                key = generateKey.returnValue()
                otp=key['OTP']
                activation_key=key['totp']
                old.otp = otp
                old.activation_key = activation_key
                old.save()
                email = old.email
                
                emailtext = """<p>Your One Time Password (OTP ) is <span
                            style="font-weight: bolder; font-size: larger; background-color: rgb(230, 233, 236); padding: 4px;">{}</span>
                    </p>
                    <br>
                    <p>This otp is valid for 1 day only.</p>
                    <em>Thank you</em><br />
                    <em>Team <b>Smart Wakil</b></em>""".format(otp,)
                send_email = send_mail(
                    # title:
                    "One Time Password.",
                    # message:
                    emailtext,
                    # from:
                    settings.EMAIL_HOST_USER,
                    # to:
                    [email],
                    html_message=emailtext
                )
                return Response({
                    'status': True,
                    'detail': 'OTP has been send to your email address.',
                    'err_code':  1
                })
            else:
                return Response({
                    'status': False,
                    'detail': 'First proceed via Registration.',
                    'err_code':  2
                })
        else:
            return Response({
                'status': False,
                'detail': 'Please provide both phone and otp for validations',
                'err_code':  3
            })

    def generateOTP(self):
        digits = "0123456789"
        OTP = ""
        for i in range(4):
            OTP += digits[math.floor(random.random() * 10)]
        return OTP

class generateKey:
    @staticmethod
    def returnValue():
        secret = pyotp.random_base32()        
        totp = pyotp.TOTP(secret, interval=86400)
        OTP = totp.now()
        return {"totp":secret,"OTP":OTP}