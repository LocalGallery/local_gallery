from django import forms
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=40)
    logo_file = models.ImageField('Logo',
                                  upload_to='photos/logos')
    center = models.PointField()
    zoom_level = models.IntegerField()

    def __str__(self):
        return "[{}]: {}".format(self.id, self.name)


class Location(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE,
                                related_name="locations")
    name = models.CharField(max_length=100)
    point = models.PointField()
    information = models.TextField(blank=True)

    class Meta:
        unique_together = (('project', 'name'))

    def __str__(self):
        return "[{}]: {} - {}".format(self.id, self.project.name, self.name)

    def first_photo(self):
        try:
            return self.photos.all()[0]
        except IndexError:
            return None


class Photo(models.Model):
    def get_path(instance, filename):
        return 'photos/local_photos/' + str(instance.location.project.id) + '/' +\
                    str(instance.location.id) + '/' + filename

    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE,
                                 related_name="photos")
    photo_file = models.ImageField('Local Photo',
                                   upload_to=get_path)
    date_taken = models.DateField(null=True, blank=True)
    long_desc = models.TextField()
    tags_array = ArrayField(models.CharField(max_length=20), default=list)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('location', 'date_taken', 'name')
