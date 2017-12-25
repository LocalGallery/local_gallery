from django.contrib.gis.geos import Point
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import html
from django.utils.html import linebreaks
from rest_framework import generics

from archive_manager import serializers
from archive_manager.forms import LocationForm
from .forms import PostPhoto
from .models import Location


def home(request):
    locations = Location.objects.all()
    return render(request, 'archive_manager/index.html',
                  {'locations': locations})


def post_new(request):
    if request.method == 'GET':
        form = PostPhoto(request.GET, request.FILES)
        return render(request, 'archive_manager/post_edit.html',
                      {'form': form})
    elif request.method == 'POST':
        form = PostPhoto(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # if request.user.is_authenticated:
            #     post.author = request.user
            post.save()
            return HttpResponseRedirect(
                reverse('archive_gallery', args=[post.location.id]))
        else:
            return render(request, 'archive_manager/post_edit.html',
                          {'form': form})


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
    import time
    time.sleep(1)
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            # TODO: check if is in Israel
            p = Point([form.cleaned_data['lng'], form.cleaned_data['lat']])
            form.instance.point = p
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
    serializer_class = serializers.LocationSerializer


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer
