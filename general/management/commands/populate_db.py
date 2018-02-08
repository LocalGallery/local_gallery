import glob
import json
import random
from pathlib import Path

import silly
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point, Polygon
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError

from locations.models import Location, Photo
from projects.models import Project

SAMPLE_PROJECTS_FILE = Path(
    settings.BASE_DIR) / "general" / "sample_projects.geojson"

IMG_PATH = Path(settings.BASE_DIR) / "general" / "dummy_data"


def load_projects(data):
    for feat in data['features']:
        yield {
            'name': feat['properties']['name'],
            'slug': feat['properties']['slug'],
            'polygon': Polygon(*feat['geometry']['coordinates']),
        }


class Command(BaseCommand):
    help = "Populate database tables."

    num_of_locations_per_project = 5
    num_of_photos_per_location = 10

    def handle(self, *args, **options):
        images = glob.glob(f"{IMG_PATH}/image*.jpeg")

        try:
            User.objects.create_superuser('sysop', '', 'sysop')
        except IntegrityError:
            pass

        with SAMPLE_PROJECTS_FILE.open() as f:
            for i, proj in enumerate(load_projects(json.load(f))):
                with transaction.atomic():
                    print(proj['slug'])
                    project = Project()
                    project.name = proj['name']
                    project.slug = proj['slug']
                    project.geom = proj['polygon']
                    project.center = proj['polygon'].centroid
                    f = (IMG_PATH / f"logo_{i + 1:04d}.jpeg").open("rb")
                    project.logo_file.save(f"logo{i + 1}.jpeg", File(f))
                    project.save()

                    for location_id in range(
                            self.num_of_locations_per_project):
                        location = Location()
                        location.project = project
                        location.name = silly.a_thing()
                        x0, y0, x1, y1 = project.geom.extent
                        x = random.uniform(x0, x1)
                        y = random.uniform(y0, y1)
                        location.point = Point(x, y)
                        location.information = silly.sentence()
                        location.save()

                        for photo_id in range(
                                random.randint(0,
                                               self.num_of_photos_per_location)):
                            photo = Photo()
                            photo.name = silly.a_thing()
                            photo.location = location
                            photo.date_taken = silly.datetime().date()
                            photo.lond_desc = silly.paragraph()
                            with open(random.choice(images), "rb") as f:
                                photo.photo_file.save("random.jpg", File(f))
                            photo.save()
