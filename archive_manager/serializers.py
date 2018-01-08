from archive_manager.models import Location
from rest_framework import serializers

from .models import Photo


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'project', 'name', 'point', 'information')
        read_only_fields = ('project',)


class LocationPhotoSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(source='location.project.id',
                                                    many=False,
                                                    read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(source='location.id',
                                                     many=False,
                                                     read_only=True)
    location_name = serializers.PrimaryKeyRelatedField(source='location.name',
                                                       many=False,
                                                       read_only=True)
    name = serializers.CharField(max_length=100, default='photo desc')
    photo_file = serializers.ImageField()
    date_taken = serializers.DateField()
    created_at = serializers.DateTimeField()
    long_desc = serializers.CharField()
    # TODO: tags_array

    class Meta:
        model = Photo
        fields = ('id',
                  'project_id',
                  'location_id',
                  'location_name',
                  'name',
                  'created_at',
                  'date_taken',
                  'photo_file',
                  'long_desc')


class PhotoSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(source='location.project.id',
                                                    many=False,
                                                    read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(source='location.id',
                                                     many=False,
                                                     read_only=True)
    location_name = serializers.PrimaryKeyRelatedField(source='location.name',
                                                       many=False,
                                                       read_only=True)
    name = serializers.CharField(max_length=100, default='photo desc')
    photo_file = serializers.ImageField()
    date_taken = serializers.DateField()
    created_at = serializers.DateTimeField()
    long_desc = serializers.CharField()
    # TODO: tags_array

    class Meta:
        model = Photo
        fields = ('id',
                  'project_id',
                  'location_id',
                  'location_name',
                  'name',
                  'created_at',
                  'date_taken',
                  'photo_file',
                  'long_desc')
