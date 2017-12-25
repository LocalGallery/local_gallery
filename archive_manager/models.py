from django import forms
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    point = models.PointField()
    information = models.TextField(blank=True)

    def __str__(self):
        return "[{}]: {}".format(self.id, self.name)

    def first_photo(self):
        try:
            return self.photos.all()[0]
        except IndexError:
            return None


class Photo(models.Model):
    name = models.TextField(max_length=100)
    photo_file = models.ImageField('Local Photo',
                                   upload_to='photos/local_photos')
    location = models.ForeignKey('Location', on_delete=models.CASCADE,
                                 related_name="photos")
    date_taken = models.DateField()
    date_added = models.DateField(blank=True, null=True)
    long_desc = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 10, 'rows': 20}))
    tags_array = ArrayField(models.CharField(max_length=20), default=list)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('location', 'date_taken', 'name')
