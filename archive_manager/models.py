from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django import forms

from datetime import datetime
class Location(models.Model):
    name = models.CharField(max_length=100)
    point = models.PointField()
    information = models.TextField(max_length=15,default='localtion info')


class Photo(models.Model):
    name = models.TextField(max_length=100,default='photo desc')
    photo_file = models.ImageField('Local Photo', upload_to='photos/local_photos')
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    date_taken = models.DateField()
    date_added = models.DateField(blank=True, null=True)
    long_desc = forms.CharField(widget=forms.Textarea(attrs={'cols': 10, 'rows': 20}))
    tags_array = ArrayField(models.CharField(max_length=20),default=list)