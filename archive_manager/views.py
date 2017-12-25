from django.conf import settings
from django.contrib.gis.geos import Point
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import html
from django.utils.html import linebreaks
from rest_framework import generics

from .forms import PostPhoto, LocationForm
from .models import Location
from .serializers import LocationSerializer


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


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
