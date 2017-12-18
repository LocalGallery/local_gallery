from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.urls import reverse

from .models import Location, Photo

# Create your views here.
from .forms import PostPhoto


def home(request):
    locations = Location.objects.all()
    photos = Photo.objects.all()
    return render(request, 'archive_manager/index.html', {'locations': locations, 'photos': photos})


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
        'archive_photos': location.photo_set.all(),
        })
