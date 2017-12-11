from django import forms
from django.forms import ModelForm, Textarea
from .models import Photo, Location


class PostPhoto(forms.ModelForm):

    class Meta:
        model = Photo
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_file': forms.FileInput(attrs={'class': 'form-control-file'}),
            'date_taken': forms.DateInput(attrs={'class': 'form-'}),
        }
        fields = ('name', 'photo_file', 'date_taken', 'location')
