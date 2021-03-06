import datetime

from django import forms

from locations.models import Photo, Location


def last_years():
    first_year = datetime.datetime.now().year - 200
    return list(range(datetime.datetime.now().year, first_year, -1))


class CreatePhotoForm(forms.ModelForm):
    class Meta:
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


class UpdatePhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = (
            'name',
            'long_desc',
            'date_taken',
            'location',
        )


class LocationForm(forms.ModelForm):
    lat = forms.DecimalField(widget=forms.HiddenInput)
    lng = forms.DecimalField(widget=forms.HiddenInput)

    class Meta:
        model = Location
        widgets = {
            'information': forms.Textarea(attrs={'cols': 25, 'rows': 5}),
        }
        fields = (
            'name',
            'information',
        )
