from django.test import TestCase
from rest_framework import status

from api.application.images_handle_events_service import ImagesHandleEventsService
from api.domain.images_models import ImageInfo, VIEWS_VALUE, CLICKS_VALUE
from api.domain.serializers.trackers import TrackEventBodySerializer


class ImagesHandleEventsServiceTest(TestCase):

    def setUp(self):
        self.image = ImageInfo.objects.create(name='image_3', url='https://image_3.com')
        self.service = ImagesHandleEventsService
        self.serializer_class = TrackEventBodySerializer

    def test_click_weight_update(self):
        data_click = {'event_type': 'click'}
        service = self.service(self.image.id, data_click, self.serializer_class)
        response = service.handle_image_events()
        refresh_image = ImageInfo.objects.get(id=self.image.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(refresh_image.weight, CLICKS_VALUE)

    def test_view_weight_update(self):
        data_click = {'event_type': 'view'}
        service = self.service(self.image.id, data_click, self.serializer_class)
        response = service.handle_image_events()
        refresh_image = ImageInfo.objects.get(id=self.image.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(refresh_image.weight, VIEWS_VALUE)
