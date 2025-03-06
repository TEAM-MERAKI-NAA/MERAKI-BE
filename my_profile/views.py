from django.shortcuts import render
from .models import *
# from rest_framework.permissions import IsAuthenticated
from rest_framework import request, viewsets
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
import time

# Create your views here
class MyProfileViewset(viewsets.ModelViewSet):
    queryset=MyProfile.objects.all()
    serializer_class=MyProfileSerializer

    def perform_create(self, serializer):
        user = self.request.user
        member = MyProfile.objects.get(pk=user.pk)
        serializer.save(user=member)

    def list(self, request, *args, **kwargs):
        queryset = MyProfile.objects.filter(user=request.user)
        res = MyProfileSerializer(queryset,many=True).data
        return Response(res)

class GetProfileDataViewSet(APIView):
    def get(self, request,  format=None):
        current_user = request.user
        memberdata = MyProfile.objects.filter(
            pk=current_user.pk
        ).first()
        if memberdata:
            if memberdata.image: 
                image = request.build_absolute_uri(memberdata.image.url)
            else:
                image = ''
            resp_data = {   
                'first_name': memberdata.first_name,
                'last_name': memberdata.last_name,
                'username': memberdata.user.username,
                'image': image
            }
        else:
            resp_data = {   
                'first_name': '',
                'last_name': '',
                'username': '',
                'image': ''
            }
        print(resp_data)
        return Response(resp_data)

class ProfileEditViewSet(APIView):
    def post(self, request,  format=None):
        datas = request.data
        profile = MyProfile.objects.filter(pk=request.user.pk)
        profile.update(**datas)
        return Response(datas)



    # def post(request, user_id):
    #     user = User.objects.get(pk=user_id)
    #     user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    #     user.save()
class UploadProfileImageViewSet(APIView):
    def post(self, request,  format=None):
        # time.sleep(5)
        datas = request.data
        profile = MyProfile.objects.filter(pk=request.user.pk).first()
        if not profile:
            profile = MyProfile(
                pk=request.user.pk
            )
        # serializer = MyProfileImageSerializer(data=datas)
        print(profile)
        serializer = MyProfileImageSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(
                image=request.data.get('image')
            )
        # done = profile.update(**datas)
        return Response(serializer.data)
