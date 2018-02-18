import operator
from functools import reduce

from django.db.models import Q
from rest_framework import generics

from locations.models import Location, Photo
from locations.serializers import LocationSerializer, LocationPhotoSerializer, \
    PhotoSerializer
from projects.models import Project


class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        project = self.kwargs.get('pj_id')
        queryset = self.queryset.filter(project=project)
        return queryset

    def perform_create(self, serializer):
        project = Project.objects.all().filter(id=self.kwargs.get('pj_id'))[0]
        serializer.save(project=project)


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        project = self.kwargs.get('pj_id')
        id_ = self.kwargs.get('pk')
        queryset = self.queryset.filter(id=id_, project=project)
        return queryset


def get_related_project_id(location_id):
    return Location.objects.filter(id=location_id).values_list('project',
                                                               flat=True)


class LocationPhotoList(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = LocationPhotoSerializer

    def get_queryset(self):
        location_id = self.kwargs.get('pk')
        project_id = self.kwargs.get('pj_id')
        if project_id in get_related_project_id(location_id):
            queryset = self.queryset.filter(location_id=location_id)
        else:
            queryset = Photo.objects.none()
        return queryset

    def perform_create(self, serializer):
        location = Location.objects.all().filter(id=self.kwargs.get('pk'))[0]
        serializer.save(location=location)

def get_locations(project_id):
    return Location.objects.filter(project=project_id).values_list('id',
                                                                   flat=True)

class PhotoList(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('pj_id')
        queryset = self.queryset.filter(reduce(operator.or_,
                                               (Q(location_id=id) for id in
                                                get_locations(project_id))))
        return queryset



def get_related_location_id(photo_id):
    return Photo.objects.filter(id=photo_id).values_list('location',
                                                         flat=True)


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


    def get_queryset(self):
        photo_id = self.kwargs.get('pk')
        project_id = self.kwargs.get('pj_id')
        if project_id in get_related_project_id(
                get_related_location_id(photo_id)[0]):
            queryset = self.queryset.filter(id=photo_id)
        else:
            queryset = Photo.objects.none()
        return queryset
