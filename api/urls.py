from django.urls import path

from api.infrastructure.images_view import GetAllImagesGridView, HandlingImageEventsView
from api.infrastructure.ping_view import PingView

app_name = 'api'

urlpatterns = [
    path('ping', PingView.as_view()),
    path('images', GetAllImagesGridView.as_view()),
    path('images/<uuid:image_id>/events', HandlingImageEventsView.as_view()),
]
