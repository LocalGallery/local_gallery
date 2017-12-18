from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django import forms

from datetime import datetime
class Location(models.Model):
    name = models.CharField(max_length=100)
    point = models.PointField()
    information = models.TextField(max_length=15,default='localtion info')

    def __str__(self):
        return "[{}]: {}".format(self.id, self.name)

    def first_three(self):
        return self.photos.all()[:3]


class Photo(models.Model):
    name = models.TextField(max_length=100,default='photo desc')
    photo_file = models.ImageField('Local Photo', upload_to='photos/local_photos')
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name="photos")
    date_taken = models.DateField()
    date_added = models.DateField(blank=True, null=True)
    long_desc = forms.CharField(widget=forms.Textarea(attrs={'cols': 10, 'rows': 20}))
    tags_array = ArrayField(models.CharField(max_length=20),default=list)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('location', 'date_taken', 'name')