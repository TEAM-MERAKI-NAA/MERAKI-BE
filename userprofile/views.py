from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import UserProfileSerializer

# Create your views here.

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile_view')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'userprofile/profile.html', context)

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own profile
        return UserProfile.objects.filter(user=self.request.user)

    def get_object(self):
        # Get user's own profile
        return get_object_or_404(UserProfile, user=self.request.user)

    def perform_update(self, serializer):
        # Update the profile
        serializer.save()

    @action(detail=False, methods=['GET'])
    def me(self, request):
        # Get current user's profile
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        # Override list to return only the user's profile
        return self.me(request)
