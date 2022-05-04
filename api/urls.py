from django.urls import path

from api.infrastructure.ping_view import PingView

app_name = 'api'

urlpatterns = [
    path('ping', PingView.as_view()),
]
