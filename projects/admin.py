from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from projects.models import Project

admin.site.register(Project, OSMGeoAdmin)
