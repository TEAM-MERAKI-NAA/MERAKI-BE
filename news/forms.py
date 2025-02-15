from django import forms
from django.db import models
from .models.newsletter_category import NewsletterCategory

from .models.news import News

class NewsForm(forms.ModelForm):
    # long_description = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = News
        fields = ['user', 'title','short_description','long_description','main_categories','categories',\
            'image']
    title = forms.CharField()
    categories = forms.ModelMultipleChoiceField(
        queryset=NewsletterCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple
)