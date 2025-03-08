from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GetProfileDataViewSet, MyProfileViewset, ProfileEditViewSet, UploadProfileImageViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'myprofile', MyProfileViewset)

urlpatterns = [
    path(r'api/', include(router.urls)),
    path('api/profiledata', GetProfileDataViewSet.as_view(), name='profile_data'),
    path('api/editprofile', ProfileEditViewSet.as_view(), name='edit_profile'),
    path('api/upload-profile-image', UploadProfileImageViewSet.as_view(), name='upload_profile_image'),
    
]
