from django.urls import path

from .consumers import GraphConsumer

ws_urlpatterns = [
    path('ws/tank/', GraphConsumer.as_asgi())
]