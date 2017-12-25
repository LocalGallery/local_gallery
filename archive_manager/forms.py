import datetime

from django import forms
from .models import Photo, Location


class PostPhoto(forms.ModelForm):
    class Meta:
        def last_years():
            first_year = datetime.datetime.now().year - 200
            return list(range(datetime.datetime.now().year, first_year, -1))

        model = Photo
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_file': forms.FileInput(
                attrs={'class': 'form-control-file'}),
            'date_taken': forms.SelectDateWidget(years=last_years(),
                                                 attrs={'class': 'form-'}),
        }
        fields = ('name', 'photo_file', 'date_taken', 'location')


class LocationForm(forms.ModelForm):
    lat = forms.DecimalField(widget=forms.HiddenInput)
    lng = forms.DecimalField(widget=forms.HiddenInput)

    class Meta:
        model = Location
        fields = (
            'name',
            'information',
        )
