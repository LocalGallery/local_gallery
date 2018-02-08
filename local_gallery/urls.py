"""local_gallery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

import locations.views
import projects.views
from locations import api_views

urlpatterns = [
    path('', projects.views.ProjectListView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('post/new/', locations.views.post_new, name='post_new'),
    path('add-location/', locations.views.create_location,
         name="create_location"),

    path('<slug:slug>/', projects.views.ProjectDetailView.as_view(),
         name='project_detail'),
    path('<slug:slug>/image/new/', locations.views.PhotoCreateView.as_view(),
         name='post_new_image'),
    path('<slug:slug>/<int:pk>/', locations.views.LocationDetailView.as_view(),
         name='location'),
    path('<slug:slug>/<int:location_pk>/<int:pk>/',
         locations.views.PhotoDetailView.as_view(),
         name='photo'),

    path('accounts/', include('django.contrib.auth.urls')),

]

# REST API urls:
urlpatterns += [
    path('api/<int:pj_id>/locations/',
         api_views.LocationList.as_view()),
    path('api/<int:pj_id>/locations/<int:pk>/',
         api_views.LocationDetail.as_view()),
    path('api/<int:pj_id>/locations/<int:pk>/photos/',
         api_views.LocationPhotoList.as_view()),
    path('api/<int:pj_id>/photos/', locations.api_views.PhotoList.as_view()),
    path('api/<int:pj_id>/photos/<int:pk>/',
         api_views.PhotoDetail.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
