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
from django.db.models import Q
from .models import UserOtp
from django.contrib.auth.models import BaseUserManager
from fcm_django.models import FCMDevice
import requests
from rest_framework.response import Response

#for recaptcha
import urllib
import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

from django.conf import settings


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


@permission_classes((AllowAny, ))
class UserCreateViewSet(APIView):

    @transaction.atomic
    def post(self, request,  format=None):
        username = request.data.get('username', False)
        data = {}
        email = True
        if '@' in username:
            email = BaseUserManager.normalize_email(username)
            data['email'] = email
            data['username'] = username
        else:
            phone_number = username
            data['phone_number'] = phone_number
            data['username'] = username
            email = False

        query = Q(username=username)
        query.add(Q(email=username), Q.OR)
        query.add(Q(phone_number=username), Q.OR)

        checkuser = User.objects.filter(query)
        errors = dict()
        if checkuser:
            errors['username'] = 'User already exists.'
            errors['active'] = checkuser.is_active
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        key = generateKey.returnValue()
        data['otp'] = key['OTP']
        data['activation_key'] = key['totp']
        data['is_staff'] = False
        data['is_active'] = False
        data['is_superuser'] = False
        user = User.objects.create(
            **data
        )
        user.set_password(data['activation_key'])
        user.save()

        if email:
            self.sendOtpEmail(data['username'],key)
        else:
            self.sendOtpMobile(data['username'],key)

        resp = {
            'status': True,
            'resp': {'user': user}
        }
        
        return Response(resp, status=status.HTTP_200_OK)

    def sendOtpEmail(self, email, key):
        emailtext = """<p>Your One Time Password (OTP ) is <span
                            style="font-weight: bolder; font-size: larger; background-color: rgb(230, 233, 236); padding: 4px;">{}</span>
                    </p>
                    <br>
                    <p>This otp is valid for 1 day only.</p>
                    <em>Thank you</em><br />
                    <em>Team <b>Finnove</b></em>""".format(key['OTP'],)

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

    def sendOtpMobile(self, phone_number, key):

        pass

@permission_classes((AllowAny, ))
class UserOtpRegistration(APIView):
    @transaction.atomic
    def post(self, request,  format=None):
        username = request.data.get('username', False)
        data = {}
        email = False
        errors = dict()
        if username:
            if '@' in username:
                email = BaseUserManager.normalize_email(username)
                data['username'] = email
                email = True
            else:
                data['username'] = username
                email = False
        else:
            # errors['username'] = 'Empty username'
            errors['status'] = False
            errors['detail'] = 'Username shouldnot be empty'
            return Response(errors, status=status.HTTP_200_OK)

        query = Q(username=username)
        query.add(Q(email=username), Q.OR)
        query.add(Q(phone_number=username), Q.OR)

        checkuser = User.objects.filter(query)
        errors = dict()
        if checkuser.exists():
            checkuser = checkuser.first()
            errors['username'] = 'User already exists.'
            errors['status'] = False
            errors['detail'] = 'User already exists.'
            return Response(errors, status=status.HTTP_200_OK)

        oldOtp = UserOtp.objects.filter(username=username)
        count = 1
        if oldOtp.exists():
            oldOtp = oldOtp.first()
            count = oldOtp.count
            if count > 10:
                return Response({
                    'status': False,
                    'detail': 'Sending OTP error Limit exceeded. Please contact customer support'
                })
            count = count + 1
        
        key = generateKey.returnValue()
        data['otp'] = key['OTP']
        data['activation_key'] = key['totp']
        data['count'] = count
        if oldOtp:
            oldOtp.otp = key['OTP']
            oldOtp.activation_key = key['totp']
            oldOtp.count = count
            oldOtp.save()
        else: 
            otp = UserOtp.objects.create(
                **data
            )
            print('tst', otp)

        if email:
            self.sendOtpEmail(username, data)
        else:
            self.sendOtpMobile(username, data)

        resp = {
            'status': True,
            'resp': {'user': username}
        }
        
        return Response(resp, status=status.HTTP_200_OK)


    def sendOtpEmail(self, email, data):
        emailtext = """<p>Your One Time Password (OTP ) is <span
                            style="font-weight: bolder; font-size: larger; background-color: rgb(230, 233, 236); padding: 4px;">{}</span>
                    </p>
                    <br>
                    <p>This otp is valid for 1 day only.</p>
                    <em>Thank you</em><br />
                    <em>Team <b>Finnove</b></em>""".format(data['otp'],)

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

    def sendOtpMobile(self, phone_number, data):

        token = '5f47e9e2e4d4cf70b01a2de2a6fcfb34f5fb4e09b3483a47f9c28a8d0411ae7a'
        smsfrom = '31001'
        smsto = [phone_number]
        message = """Your One Time Password (OTP ) is {}
                    """.format(data['otp'],)
        response_json = []
        try:
            r = requests.post(
                "https://sms.aakashsms.com/sms/v3/send/",
                data={'auth_token' : token,
                    'from'  : smsfrom,
                    'to'    : smsto,
                    'text'  : message})
            response_json = r.json()
            if response_json['response_code'] == 201 or response_json['response_code'] == 200:
                response_json = {"sucess": True,"message": r.json()}
                pass
            else:
                raise ValueError(response_json['response'])
        except ValueError as ve:
            return Response({"sucess": False,"message": str(ve)}) 
        except Exception as e:
            return Response({"sucess": False,"message": str(e)}) 

class ValidateOTP(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        otp = request.data.get('otp', False)
        username = request.data.get('username', False)

        old = UserOtp.objects.filter(username__iexact=username)
        if old.exists():
            old = old.first()
            # count = old.count
            _otp = old.otp
            if int(otp) != int(_otp):
                # count = count + 1
                # old.count = count 
                # old.save()
                return Response({
                    "status": False, 
                    "detail": "Invalid otp"
                    })
            else:
                activation_key = old.activation_key
                totp = pyotp.TOTP(activation_key, interval=86400)
                verify = totp.verify(otp)
                if verify:
                    old.validated = True
                    old.save()
                    return Response({
                        'status': True,
                        'detail': 'OTP verified'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect, please try again'
                    })
        else:
            return Response({
                'status': False,
                'detail': 'User doesnot exists, please try again'
            })
            

    def sendEmail(self, user):
        emailtext = """
                    <h1>Welcome <strong>{}</strong></h1>
                    <p>Your account successfully activated. Now Please update your password!!
                    </p>
                    <br>
                    <em>Thank you</em><br />
                    <em>Team <b>Finnove</b></em>""".format(user.username,)

        send_email = send_mail(
            "One Time Password.",
            emailtext,
            settings.EMAIL_HOST_USER,
            [user.email],
            html_message=emailtext
        )


class UserRegisterAfterOtp(APIView):
    permission_classes = [AllowAny]
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', False)
        password = request.data.get('password', False)
        confirm_password = request.data.get('confirm_password', 'no')
        if password != confirm_password:
            return Response({
                'status': False,
                'detail': 'Password Mismatch'
            })

        old = UserOtp.objects.filter(username__iexact=username)
        if username and password:
            if old.exists():
                old = old.first()
                validated = old.validated
                if validated:
                    email = False
                    data = {}
                    if '@' in username:
                        email = BaseUserManager.normalize_email(username)
                        data['username'] = email
                        data['email'] = email
                        data['phone_number'] = ''
                        email = True
                    else:
                        data['username'] = username
                        data['phone_number'] = username
                        data['email'] = ''
                        email = False
                    query = Q(username=username)
                    query.add(Q(email=username), Q.OR)
                    query.add(Q(phone_number=username), Q.OR)
                    olduser = User.objects.filter(
                        query
                    )
                    if olduser:
                        return Response({
                            'status': False,
                            'detail': 'User already registered. Please Login'
                        })
                    user = User.objects.create(
                        username = data['username'],
                        email = data['email'],
                        phone_number=data['phone_number'],
                        is_staff=False,
                        is_superuser=False,
                        is_active=True
                    )
                    user.set_password(password)
                    user.save()

                    # uncomment this and check with registration if profile is created or not
                    # myprofile = MyProfile.objects.create(
                    #     user = user
                    # )
                    # myprofile.save()

                    old.delete()
                    self.sendEmail(user)
                    device = FCMDevice()
                    return Response({
                        'status': True,
                        'detail': 'Successfully registered'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'Please validate the otp first'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Please verify the phone first'
                })
        else:
            return Response({
                'status': False,
                'detail': 'Both username and password are not correct'
            })

    def sendEmail(self, user):
        emailtext = """
                    <h1>Welcome <strong>{}</strong></h1>
                    <p>Your account has been successfully created.!!
                    </p>
                    <br>
                    <em>Thank you</em><br />
                    <em>Team <b>Finnove</b></em>""".format(user.username,)

        send_email = send_mail(
            "Registration.",
            emailtext,
            settings.EMAIL_HOST_USER,
            [user.email],
            html_message=emailtext
        )
        


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


class generateKey:
    @staticmethod
    def returnValue():
        secret = pyotp.random_base32()        
        totp = pyotp.TOTP(secret, interval=86400, digits=6,)
        OTP = totp.now()
        return {"totp":secret,"OTP":OTP}

class VerifyUserIfLoggedIn(APIView):
    def get(self, request):
        currentuser = request.user
        resp = {
                    'displayName': currentuser.username,
                    'email': currentuser.email,
                    'is_active': currentuser.is_active,
                    'name': currentuser.username
                }
        # serializer = UserManagerSerializer(currentuser)
        # serializerdata = serializer.data
        return Response(resp)


# forgot password
@permission_classes((AllowAny, ))
class ForgotPasswordSendOtp(APIView):
    @transaction.atomic
    def post(self, request,  format=None):
        username = request.data.get('username', False)
        data = {}
        errors = dict()
        email = False
        if username:
            if '@' in username:
                username = BaseUserManager.normalize_email(username)
                data['username'] = username
                email = True
            else:
                data['username'] = username
                email = False
        else:
            errors['status'] = False
            errors['detail'] = 'Username shouldnot be empty'
            return Response(errors, status=status.HTTP_200_OK)

        query = Q(username=username)
        query.add(Q(email=username), Q.OR)
        query.add(Q(phone_number=username), Q.OR)

        checkuser = User.objects.filter(query)
        errors = dict()
        if not checkuser.exists():
            checkuser = checkuser.first()
            errors['username'] = 'User doesnot exists.'
            errors['status'] = False
            errors['detail'] = 'User doesnot exists.'
            return Response(errors, status=status.HTTP_200_OK)

        oldOtp = UserOtp.objects.filter(username=username)
        count = 1
        if oldOtp.exists():
            oldOtp = oldOtp.first()
            count = oldOtp.count
            if count > 115:
                return Response({
                    'status': False,
                    'detail': 'Sending OTP error Limit exceeded. Please contact customer support'
                })
            count = count + 1

        key = generateKey.returnValue()
        data['otp'] = key['OTP']
        data['activation_key'] = key['totp']
        data['count'] = count
        if oldOtp:
            oldOtp.otp = key['OTP']
            oldOtp.activation_key = key['totp']
            oldOtp.count = count
            oldOtp.save()
        else:
            otp = UserOtp.objects.create(
                **data
            )
        if email:
            sendOtpEmail(username, data['otp'])
        else:
            otpsent = sendOtpMobile(username, data['otp'])
           

        resp = {
            'status': True,
            'resp': {'user': username}
        }
        return Response(resp, status=status.HTTP_200_OK)


class ForgotPasswordAfterOtpVerify(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', False)
        password = request.data.get('password', False)
        confirm_password = request.data.get('confirm_password', 'no')
        if password != confirm_password:
            return Response({
                'status': False,
                'detail': 'Password Mismatch'
            })

        old = UserOtp.objects.filter(username__iexact=username)
        if username and password:
            if old.exists():
                old = old.first()
                validated = old.validated
                if validated:
                    is_email = False
                    if '@' in username:
                        is_email = True
                    else:
                        is_email = False
                    query = Q(username=username)
                    query.add(Q(email=username), Q.OR)
                    query.add(Q(phone_number=username), Q.OR)
                    olduser = User.objects.filter(
                        query
                    ).first()
                    if olduser:
                        olduser.set_password(password)
                        olduser.save()
                        old.delete()
                        return Response({
                            'status': True,
                            'detail': 'Password Changed Successfully'
                        })
                    else:
                        return Response({
                            'status': False,
                            'detail': 'User doesnot exists'
                        })
                        
                else:
                    return Response({
                        'status': False,
                        'detail': 'Please validate the otp first'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Please verify the phone / email first'
                })
        else:
            return Response({
                'status': False,
                'detail': 'Both username and password are required'
            })

def sendOtpEmail(email, otp):
    emailtext = """<p>Your One Time Password (OTP ) is <span
                        style="font-weight: bolder; font-size: larger; background-color: rgb(230, 233, 236); padding: 4px;">{}</span>
                </p>
                <br>
                <p>This otp is valid for 1 day only.</p>
                <em>Thank you</em><br />
                <em>Team <b>Fynov</b></em>""".format(otp)
    send_mail(
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


def sendOtpMobile(phone_number, otp):
    token = '5f47e9e2e4d4cf70b01a2de2a6fcfb34f5fb4e09b3483a47f9c28a8d0411ae7a'
    smsfrom = '31001'
    smsto = [phone_number]
    message = """Your One Time Password (OTP ) is {}
                    """.format(otp,)
    response_json = []
    try:
        r = requests.post(
                "https://sms.aakashsms.com/sms/v3/send/",
                data={'auth_token': token,
                      'from': smsfrom,
                      'to': smsto,
                      'text': message})
        response_json = r.json()
        if response_json['response_code'] == 201 or response_json['response_code'] == 200:
            return True
        else:
            return False
    except ValueError as ve:
        return False
    except Exception as e:
        return False
