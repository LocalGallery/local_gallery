from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Location, Photo

admin.site.register(Location, OSMGeoAdmin)
admin.site.register(Photo)
