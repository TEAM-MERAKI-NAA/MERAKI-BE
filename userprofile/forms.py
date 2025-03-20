from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_image', 'gender', 'nationality', 'province', 'first_name', 'last_name']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        } 