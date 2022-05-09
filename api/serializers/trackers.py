from rest_framework import serializers

from api.models import TrackEventBody


class TrackEventBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackEventBody
        fields = ['event_type', 'timestamp']
