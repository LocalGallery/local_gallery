from django import forms
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=40)
    logo_file = models.ImageField('Logo', upload_to='photos/logos')
    geom = models.PolygonField()
    center = models.PointField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project_detail", args=(self.slug,))

    def bounds(self):
        """Prepare extent to work with leaflet's LatLngBounds"""
        x0, y0, x1, y1 = self.geom.extent
        return [[y0, x0], [y1, x1]]


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

    def get_absolute_url(self):
        return reverse('location', args=(self.project.slug, self.pk))

    def first_photo(self):
        try:
            return self.photos.all()[0]
        except IndexError:
            return None


class Photo(models.Model):
    def get_path(instance, filename):
        return 'photos/local_photos/' + str(
            instance.location.project.id) + '/' + \
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
