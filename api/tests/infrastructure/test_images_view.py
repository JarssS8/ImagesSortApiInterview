import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.domain.images_models import ImageInfo


class ImagesViewTest(TestCase):
    client = APIClient()

    def create_images(self):
        return [
            ImageInfo.objects.create(name='image_1', url='http://image_1.com'),
            ImageInfo.objects.create(name='image_2', url='http://image_2.com'),
            ImageInfo.objects.create(name='image_3', url='http://image_3.com'),
        ]

    def test_no_images(self):
        response = self.client.get('/images', format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        result = json.loads(response.content)
        self.assertIn('message', result)
        self.assertEqual("No images found", result['message'])

    def test_get_images(self):
        self.create_images()

        response = self.client.get('/images', {}, format('json'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = json.loads(response.content)
        self.assertIn('images', result)
        self.assertEqual(len(result['images']), ImageInfo.objects.count())

    def post_events(self, image_id, data):
        return self.client.post('/images/{uuid}/events'.format(uuid=image_id), data,
                                content_type='application/json')

    def test_handle_click_event(self):
        image = self.create_images()[0]
        data_click = json.dumps({'event_type': 'click'})
        response = self.post_events(image.id, data_click)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        result = response.data
        self.assertIn('message', result)
        self.assertEqual("Event received", result['message'])

    def test_handle_view_event(self):
        image = self.create_images()[0]
        data_view = json.dumps({'event_type': 'view'})
        response = self.post_events(image.id, data_view)
        status_code = response.status_code
        result = response.data
        self.assertEqual(status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn('message', result)
        self.assertEqual("Event received", result['message'])

    def test_handle_invalid_event(self):
        image = self.create_images()[0]
        data_view = json.dumps({'event_type': 'touch'})
        response = self.post_events(image.id, data_view)
        status_code = response.status_code
        result = response.data
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', result)
        self.assertEqual("There request payload is not well formed", result['message'])

    def test_handle_invalid_image_id(self):
        data_view = json.dumps({'event_type': 'view'})
        response = self.post_events("b6dd4f5b-5fe7-4dbd-b500-c58806d54bdd", data_view)
        status_code = response.status_code
        result = response.data
        self.assertEqual(status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('message', result)
        self.assertEqual("There are no image with the specified ID", result['message'])
