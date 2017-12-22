from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.urls import reverse

from rest_framework import generics


from .models import Location, Photo
from archive_manager import serializers

# Create your views here.
from .forms import PostPhoto


def home(request):
    locations = Location.objects.all()
    return render(request, 'archive_manager/index.html', {'locations': locations})


def post_new(request):
    if request.method == 'GET':
        form = PostPhoto(request.GET, request.FILES)
        return render(request, 'archive_manager/post_edit.html', {'form': form})
    elif request.method == 'POST':
        form = PostPhoto(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
        # if request.user.is_authenticated:
        #     post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('archive_gallery', args=[post.location.id]))
        else:
            return render(request, 'archive_manager/post_edit.html', {'form': form})


def archive_gallery(request, id):
    location = get_object_or_404(Location, id=id)
    # photos =
    # all_photos = Photo.objects.filter(location=location)
    # archive_photos = [photo for photo in all_photos if photo.photo_location.id == id]
    return render(request, "archive_manager/archive_gallery.html", {
        'location': location,
        'archive_photos': location.photos.all(),
        })


class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer
