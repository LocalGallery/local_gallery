from django import forms
from django.forms import ModelForm, Textarea
from .models import Photo, Location


class PostPhoto(forms.ModelForm):

    class Meta:
        model = Photo
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'photo_description': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_file': forms.FileInput(attrs={'class': 'form-control-file'}),
            'photo_date_taken': forms.DateInput(attrs={'class': 'form-'}),
        }
        fields = ('photo_description', 'photo_file', 'photo_date_taken')
