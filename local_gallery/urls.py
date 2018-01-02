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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from archive_manager import views

urlpatterns = [
    path('', views.home, name="home"),
    path('admin/', admin.site.urls),
    path('post/new/', views.post_new, name='post_new'),
    path('archive-gallery/<int:id>/', views.archive_gallery,
         name="archive_gallery"),
    path('add-location/', views.create_location, name="create_location"),
]

# REST API urls:
urlpatterns += [
    url(r'^locations/$', views.LocationList.as_view()),
    url(r'^locations/(?P<pk>[0-9]+)/$', views.LocationDetail.as_view()),
    url(r'^locations/(?P<pk>[0-9]+)/photos/$', views.LocationPhotoList.as_view()),
    url(r'^photos/$', views.PhotoList.as_view()),
    url(r'^photos/(?P<pk>[0-9]+)/$', views.PhotoDetail.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
