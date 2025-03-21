from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_image', 'gender', 'nationality', 'province']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        } 