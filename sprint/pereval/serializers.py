from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "fam", "name", "otc", "phone"]


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'data', 'title']


class CoordinationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinations
        fields = ['id', 'pereval', 'latitude', 'longitude', 'height']


class PerevalSerializer(serializers.ModelSerializer):
    coordinations = CoordinationsSerializer()
    photo = PhotoSerializer(many=True)

    class Meta:
        model = Pereval
        fields = ['id', 'beauty_title', 'title', 'other_titles', 'connect', 'level_winter', 'level_summer',
                  'level_autumn', 'level_spring', 'coordinations', 'photo']

    def create(self, validated_data):
        pereval = Pereval.objects.create(**validated_data)
        coordinations_data = validated_data.pop('coordinations')
        photo_data = validated_data.pop('photo')
        Coordinations.object.create(pereval=pereval, **coordinations_data)
        for photo_data in photo_data:
            photo = Photo.object.create(**photo_data)
            PerevalPhoto.object.create(foto=photo, pereval=pereval)
        return pereval