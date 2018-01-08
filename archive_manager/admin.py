from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Location, Photo, Project

admin.site.register(Project, OSMGeoAdmin)
admin.site.register(Location, OSMGeoAdmin)
admin.site.register(Photo)
