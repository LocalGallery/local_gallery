from django.contrib.gis.db import models
from django.urls import reverse

from projects.models import Project


class Location(models.Model):
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
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

def get_photo_path(instance, filename):
    loc = instance.location
    return f'photos/local_photos/{loc.project.id}/{loc.id}/{filename}'


class Photo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE,
                                 related_name="photos")
    photo_file = models.ImageField('Local Photo', upload_to=get_photo_path)
    date_taken = models.DateField(null=True, blank=True)
    long_desc = models.TextField()

    class Meta:
        ordering = ('location', 'date_taken', 'name')

    def __str__(self):
        return self.name

