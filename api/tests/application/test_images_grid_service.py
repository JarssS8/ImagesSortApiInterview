from django.test import TestCase
from rest_framework import status

from api.application.images_grid_service import ImagesGridService
from api.application.images_handle_events_service import ImagesHandleEventsService
from api.domain.images_models import ImageInfo, VIEWS_VALUE, CLICKS_VALUE
from api.domain.serializers.images import ImagesGridResponseSerializer
from api.domain.serializers.trackers import TrackEventBodySerializer


class ImagesHandleEventsServiceTest(TestCase):

    def setUp(self):
        self.images = [
            ImageInfo.objects.create(name='image_1', url='http://image_1.com'),
            ImageInfo.objects.create(name='image_2', url='http://image_2.com'),
            ImageInfo.objects.create(name='image_3', url='http://image_3.com'),
            ImageInfo.objects.create(name='image_4', url='http://image_4.com'),
            ImageInfo.objects.create(name='image_5', url='http://image_5.com')
        ]
        self.service = ImagesGridService(ImagesGridResponseSerializer)

    def click_image(self, image):
        events = image.events
        events.clicks += 1
        events.save()
        image.calculate_weight()

    def view_image(self, image):
        events = image.events
        events.views += 1
        events.save()
        image.calculate_weight()

    # Check if receives all the images grid as response
    def test_check_get_grid(self):
        response = self.service.get_grid_images()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        images_response = response.data['images']
        self.assertEqual(len(images_response), ImageInfo.objects.count())

    # Check if receives all the images grid sorted by weight
    def test_check_weight_sorting(self):
        self.click_image(self.images[4])
        self.click_image(self.images[4])
        self.click_image(self.images[4])
        self.click_image(self.images[4])
        response = self.service.get_grid_images()
        images_response = response.data['images']
        first_image = ImageInfo.objects.get(id=images_response[0]['id'])
        self.assertEqual(first_image, ImageInfo.objects.order_by('-weight', '-created_at').first())

    # Check if receives all the images grid sorted by date
    def test_check_date_sorting(self):
        self.click_image(self.images[4])
        self.click_image(self.images[4])
        self.click_image(self.images[3])
        self.click_image(self.images[3])
        response = self.service.get_grid_images()
        images_response = response.data['images']
        first_image = ImageInfo.objects.get(id=images_response[0]['id'])
        self.assertEqual(first_image, ImageInfo.objects.order_by('-weight', '-created_at').first())
