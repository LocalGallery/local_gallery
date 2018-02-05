import glob
import math
import random
from pathlib import Path

import silly
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.files import File
from django.core.management.base import BaseCommand

from archive_manager.models import Project, Location, Photo

IMG_PATH = Path(settings.BASE_DIR) / "archive_manager" / "dummy_data"


class Command(BaseCommand):
    help = "Populate database tables."

    num_of_projects = 3
    num_of_locations_per_project = 5
    num_of_photos_per_location = 10

    def get_point(self):
        return Point(random.randint(0, 30), random.randint(0, 30))

    def handle(self, *args, **options):
        images = glob.glob(f"{IMG_PATH}/image*.jpeg")

        for project_id in range(self.num_of_projects):
            project = Project()
            project.name = silly.noun()
            project.slug = project.name
            project.center = self.get_point()
            project.zoom_level = 8
            f = (IMG_PATH / f"logo_{project_id + 1:04d}.jpeg").open("rb")
            project.logo_file.save(f"logo{project_id}.jpeg", File(f))
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
            f = open(random.choice(images), "rb")
            photo.photo_file.save("random.jpg", File(f))
            photo.save()
