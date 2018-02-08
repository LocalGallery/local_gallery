from django.contrib.gis.db import models
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
