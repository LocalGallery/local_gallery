from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import Point
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import html
from django.utils.html import linebreaks
from django.views.generic import CreateView, DetailView, UpdateView

from locations.forms import CreatePhotoForm, LocationForm
from locations.models import Photo, Location
from projects.models import Project
from . import forms


def post_new(request):
    if request.method == 'POST':
        # if request.user.is_authenticated:
        #     post.author = request.user
        form = CreatePhotoForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            if request.is_ajax():
                return JsonResponse({})
            return redirect('archive_gallery', post.location.id)
        if request.is_ajax():
            return JsonResponse({'errors': form.errors.get_json_data()},
                                status=400)
    else:
        form = CreatePhotoForm()

    return render(request, 'general/post_edit.html', {
        'form': form,
    })


class LocationDetailView(DetailView):
    model = Location

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object() # pylint: disable=attribute-defined-outside-init
        self.project = get_object_or_404(Project, slug=kwargs['slug'], # pylint: disable=attribute-defined-outside-init
                                         pk=self.object.project.pk)
        return super().dispatch(request, *args, **kwargs)


class PhotoMixin:
    model = Photo

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.location_id != kwargs['location_pk']:
            raise Http404()
        self.location = self.object.location
        if self.location.project.slug != kwargs['slug']:
            raise Http404()
        self.project = self.location.project
        return super().dispatch(request, *args, **kwargs)


class PhotoDetailView(PhotoMixin, DetailView):
    pass


class PhotoUpdateView(LoginRequiredMixin, PhotoMixin, UpdateView):
    form_class = forms.UpdatePhotoForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['location'].queryset = self.project.locations.all()
        return form


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = CreatePhotoForm

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, slug=kwargs['slug']) # pylint: disable=attribute-defined-outside-init
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['location'].queryset = self.project.locations.all()
        return form

    def form_invalid(self, form):
        assert False, form.errors

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        if self.request.is_ajax():
            return JsonResponse({'status': "OK"})

        return redirect(form.instance.location)


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

    return render(request,
                  'general/templates/locations/location_form.html', {
                      'form': form,
                  })
