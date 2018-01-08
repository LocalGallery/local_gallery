from functools import reduce
import operator

from django.conf import settings
from django.contrib.gis.geos import Point
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import html
from django.utils.html import linebreaks
from rest_framework import generics
from rest_framework import response

from .forms import PostPhoto, LocationForm
from .models import Location, Photo
from .serializers import LocationSerializer, LocationPhotoSerializer, PhotoSerializer


def home(request):
    locations = Location.objects.all()
    return render(request, 'archive_manager/index.html', {
        'center': settings.MAP_CENTER,
        'locations': locations,
    })


def post_new(request):
    if request.method == 'POST':
        # if request.user.is_authenticated:
        #     post.author = request.user
        form = PostPhoto(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            if request.is_ajax():
                return JsonResponse({})
            return redirect('archive_gallery', post.location.id)
        if request.is_ajax():
            return JsonResponse({'errors': form.errors.get_json_data()},
                                status=400)
    else:
        form = PostPhoto()

    return render(request, 'archive_manager/post_edit.html', {
        'form': form,
    })


def archive_gallery(request, id):
    location = get_object_or_404(Location, id=id)
    # photos =
    # all_photos = Photo.objects.filter(location=location)
    # archive_photos = [photo for photo in all_photos if photo.photo_location.id == id]
    return render(request, "archive_manager/archive_gallery.html", {
        'location': location,
        'archive_photos': location.photos.all(),
    })


def create_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            # TODO: check if is in Israel
            point = Point([form.cleaned_data['lng'], form.cleaned_data['lat']])
            form.instance.point = point
            location = form.save()
            if request.is_ajax():
                return JsonResponse({
                    'name': html.escape(location.name),
                    'info': linebreaks(location.information),
                    'lat': format(location.point.coords[1], ".5f"),
                    'lng': format(location.point.coords[0], ".5f"),
                })
            return redirect("home")
    else:
        form = LocationForm()

    return render(request, 'archive_manager/location_form.html', {
        'form': form,
    })


class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        project = self.kwargs.get('pj_id')
        queryset = self.queryset.filter(project=project)
        return queryset


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        project = self.kwargs.get('pj_id')
        id = self.kwargs.get('pk')
        queryset = self.queryset.filter(id=id, project=project)
        return queryset


class LocationPhotoList(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = LocationPhotoSerializer

    def get_related_project_id(self, location_id):
        return Location.objects.filter(id=location_id).values_list('project', flat=True)

    def get_queryset(self):
        location_id = self.kwargs.get('pk')
        project_id = self.kwargs.get('pj_id')
        if project_id in self.get_related_project_id(location_id):
            queryset = self.queryset.filter(location_id=location_id)
        else:
            queryset = Photo.objects.none()
        return queryset


class PhotoList(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_locations(self, project_id):
        return Location.objects.filter(project=project_id).values_list('id', flat=True)

    def get_queryset(self):
        project_id = self.kwargs.get('pj_id')
        queryset = self.queryset.filter(reduce(operator.or_, (Q(location_id=id) for id in self.get_locations(project_id))))
        return queryset


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_related_project_id(self, location_id):
        return Location.objects.filter(id=location_id).values_list('project', flat=True)

    def get_related_location_id(self, photo_id):
        return Photo.objects.filter(id=photo_id).values_list('location', flat=True)

    def get_queryset(self):
        photo_id = self.kwargs.get('pk')
        project_id = self.kwargs.get('pj_id')
        if project_id in self.get_related_project_id(self.get_related_location_id(photo_id)[0]):
            queryset = self.queryset.filter(id=photo_id)
        else:
            queryset = Photo.objects.none()
        return queryset