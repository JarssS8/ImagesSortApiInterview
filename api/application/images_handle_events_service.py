from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response

from ..models import ImageInfo
from ..models import TrackEventBody


class ImagesHandleEventsService:

    def __init__(self, image_id, data, serializer_class):
        self.EventTypesEnum = TrackEventBody.EventTypesEnum
        self.image_id = image_id
        self.data = data
        self.serializer_class = serializer_class
        self.codes = {
            '204': Response({"message": "Event received"}, status=status.HTTP_204_NO_CONTENT),
            '400': Response({"message": "There request payload is not well formed"},
                            status=status.HTTP_400_BAD_REQUEST),
            '404': Response({"message": "There are no image with the specified ID"}, status=status.HTTP_404_NOT_FOUND),
            '500': Response({"message": "There are an error with the server"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        }

    def handle_image_events(self):
        try:
            image_info = ImageInfo.objects.get(id=self.image_id)
            if image_info:
                return self.serialize_data(image_info)
            else:
                return self.codes['404']
        except ObjectDoesNotExist as e:
            return self.codes['404']
        except Exception as e:
            return self.codes['500']

    def serialize_data(self, image_info):
        serializer = self.serializer_class(data=self.data)
        if serializer.is_valid():
            event_type = serializer.data.get('event_type')
            types_list = self.EventTypesEnum.list()
            if event_type in types_list:
                return self.change_event_value(image_info, event_type)
            else:
                return self.codes['400']
        else:
            return self.codes['400']

    def change_event_value(self, image_info, event_type):
        events = image_info.events
        if event_type == self.EventTypesEnum.VIEW.value:
            events.views += 1
        elif event_type == self.EventTypesEnum.CLICK.value:
            events.clicks += 1
        events.save()
        image_info.calculate_weight()
        return self.codes['204']
