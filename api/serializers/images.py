from rest_framework import serializers

from api.models import ImageInfo, ImagesGridResponse, Events


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['views', 'clicks']


class ImageInfoSerializer(serializers.ModelSerializer):
    events = EventsSerializer()

    class Meta:
        model = ImageInfo
        fields = ['id', 'name', 'grid_position', 'weight', 'url', 'events', 'created_at']


class ImagesGridResponseSerializer(serializers.Serializer):
    images = ImageInfoSerializer(many=True)
