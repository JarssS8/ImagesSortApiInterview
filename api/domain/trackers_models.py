from django.db import models


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
