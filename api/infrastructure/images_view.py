from rest_framework import status
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..application.images_grid_service import ImagesGetGridService
from ..application.images_handle_events_service import ImagesHandleEventsService
from ..domain.serializers.images import ImagesGridResponseSerializer
from ..domain.serializers.trackers import TrackEventBodySerializer
from ..models import ImagesGridResponse, ImageInfo


# Return all the images related to the gallery to be displayed on the gallery.
# Ordering the query with the weight of the images, this is directly on model declaration.
class GetAllImagesGridView(APIView):
    serializer_class = ImagesGridResponseSerializer

    def get(self, request):
        images_get_grid_service = ImagesGetGridService(self.serializer_class)
        return images_get_grid_service.get_grid_images()


# Post for handle the possible new events associated with the images.
# This method also recalculate the weight of the images.
class HandlingImageEventsView(APIView):
    serializer_class = TrackEventBodySerializer

    def post(self, request, image_id):
        image_service = ImagesHandleEventsService(image_id, request.data, self.serializer_class)
        code = image_service.handle_image_events()
        return code
