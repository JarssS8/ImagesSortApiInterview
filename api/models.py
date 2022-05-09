import uuid

from django.db import models


class Events(models.Model):
    views = models.PositiveIntegerField("Views", default=0)
    clicks = models.PositiveIntegerField("Clicks", default=0)

    class Meta:
        verbose_name = 'Events'
        verbose_name_plural = 'Events'


def default_events():
    events = Events.objects.create()
    return events.pk


class ImageInfo(models.Model):
    id = models.UUIDField("Unique Image ID", primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Name", max_length=100)
    weight = models.FloatField("Weight", default=0.0)
    grid_position = models.PositiveSmallIntegerField("Grid Position", default=0)
    url = models.URLField("Image URL")
    events = models.OneToOneField(Events, on_delete=models.CASCADE, default=default_events)
    created_at = models.DateTimeField("Created At", null=False, blank=False, auto_now_add=True)

    def calculate_weight(self):
        self.weight = self.events.clicks * 0.7 + self.events.views * 0.3
        self.save()

    class Meta:
        verbose_name = 'ImageInfo'
        verbose_name_plural = 'ImagesInfo'
        ordering = ['-weight', '-created_at']


# Don't have Model parameter because it will not be into the ORM
class ImagesGridResponse():
    def __init__(self, images):
        self.images = images

    def has_images(self):
        if not self.images:
            return False
        return True


class TrackEventBody(models.Model):
    class EventTypesEnum(models.TextChoices):
        VIEW = 'view'
        CLICK = 'click'

        @classmethod
        def list(cls):
            return list(map(lambda c: c.value, cls))

    event_type = models.CharField("Event Type", max_length=5, null=False, blank=False, choices=EventTypesEnum.choices)
    timestamp = models.DateTimeField("Timestamp", null=False, blank=False, auto_now_add=True)

    class Meta:
        verbose_name = 'TrackEventBody'
        verbose_name_plural = 'TrackEventBodies'
        ordering = ['timestamp']
