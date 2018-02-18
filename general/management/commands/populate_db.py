import glob
import json
import random
from pathlib import Path

from faker import Faker
import silly
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point, Polygon
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError

from locations.models import Location, Photo
from projects.models import Project

GENERAL_PATH = Path(settings.BASE_DIR) / "general"
SAMPLE_PROJECTS_FILE = GENERAL_PATH / "sample_projects.geojson"
IMG_PATH = GENERAL_PATH / "dummy_data"


def load_projects(data):
    for feat in data['features']:
        yield {
            'name': feat['properties']['name'],
            'slug': feat['properties']['slug'],
            'polygon': Polygon(*feat['geometry']['coordinates']),
        }


class Command(BaseCommand):
    help = "Populate database tables."

    LOCATIONS_PER_PROJECT = 20
    PHOTOS_PER_LOCATION = 16

    def handle(self, *args, **options):
        fake = Faker("he_IL")
        images = glob.glob(f"{IMG_PATH}/image*.jpeg")

        try:
            User.objects.create_superuser('sysop', '', 'sysop')
        except IntegrityError:
            pass

        with SAMPLE_PROJECTS_FILE.open(encoding="utf-8") as f:
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

                    for _ in range(
                            self.LOCATIONS_PER_PROJECT):
                        location = Location()
                        location.project = project
                        location.name = fake.street_name() + " " + fake.street_name()
                        x0, y0, x1, y1 = project.geom.extent
                        x = random.uniform(x0, x1)
                        y = random.uniform(y0, y1)
                        location.point = Point(x, y)
                        location.information = silly.sentence()
                        location.save()

                        for _ in range(
                                random.randint(0,
                                               self.PHOTOS_PER_LOCATION)):
                            photo = Photo()
                            photo.name = fake.street_name()
                            photo.location = location
                            photo.date_taken = silly.datetime().date()
                            photo.lond_desc = fake.paragraphs(nb=3,
                                                              ext_word_list=None)
                            with open(random.choice(images), "rb") as f:
                                photo.photo_file.save("random.jpg", File(f))
                            photo.save()
