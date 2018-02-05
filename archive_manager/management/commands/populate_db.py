import math
import random
from urllib.request import urlopen

import silly

from django.contrib.gis.geos import Point
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand

from archive_manager.models import Project, Location, Photo


class Command(BaseCommand):
    help = "Populate database tables."

    num_of_projects = 3
    num_of_locations_per_project = 5
    num_of_photos_per_location = 10
    img_url = "http://lorempixel.com/640/480/"


    def get_photo_object(self, url):
        img = NamedTemporaryFile()
        img.write(urlopen(url).read())
        img.flush()
        return img


    def get_point(self):
        return Point(random.randint(0, 30), random.randint(0, 30))


    def handle(self, *args, **options):
        for project_id in range(self.num_of_projects):
            project = Project()
            project.name = silly.noun()
            project.slug = project.name
            project.center = self.get_point()
            project.zoom_level = 8
            project.logo_file.save("random.jpg", self.get_photo_object(self.img_url))
            project.save()

        for location_id in range(self.num_of_projects *
                self.num_of_locations_per_project):
            location = Location()
            location.project = Project.objects.get(pk=math.floor(1 +
                location_id / self.num_of_locations_per_project))
            location.name = silly.a_thing()
            location.point = self.get_point()
            location.information = silly.sentence()
            location.save()

        for photo_id in range(self.num_of_projects *
                self.num_of_locations_per_project *
                self.num_of_photos_per_location):
            photo = Photo()
            photo.name = silly.a_thing()
            photo.location = Location.objects.get(pk=math.floor(1 +
                photo_id / self.num_of_photos_per_location))
            photo.date_taken = silly.datetime().date()
            photo.lond_desc = silly.paragraph()
            photo.photo_file.save("random.jpg", self.get_photo_object(self.img_url))
            photo.save()
