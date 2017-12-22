from archive_manager.models import Location
from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers


class LocationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    point = PointField()
    information = serializers.CharField(max_length=15)

    def create(self, validated_data):
        return Location.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.point = validated_data.get('point', instance.point)
        instance.information = validated_data.get('information', instance.information)
        instance.save()
        return instance
