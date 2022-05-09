from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response

from ..domain.images_models import ImagesGridResponse
from ..models import ImageInfo
from ..models import TrackEventBody


class ImagesGetGridService:

    def __init__(self, serializer_class):
        self.serializer_class = serializer_class
        self.images_grid = ImagesGridResponse(ImageInfo.objects.all())
        self.codes = {
            '200': Response(self.serializer_class(self.images_grid).data, status=status.HTTP_200_OK),
            '404': Response({"message": "No images found"}, status=status.HTTP_404_NOT_FOUND),
            '500': Response({"message": "There are an error with the server"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        }

    # To avoid "Too broad exception clause" we should log our application, but I think it's not the main
    # point of this technical challenge
    def get_grid_images(self):
        try:
            if self.images_grid.has_images():
                return self.codes['200']
            else:
                return self.codes['404']
        except Exception as e:
            return self.codes['500']
