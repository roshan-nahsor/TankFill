from django.urls import path

from .consumers import GraphConsumer
# from .consumers import MyMqttConsumer         #mqttasgi
# from tank.consumers import MQTTConsumer     #chatGPT

ws_urlpatterns = [
    path('ws/tank/', GraphConsumer.as_asgi())
    # path('ws/tank/', MyMqttConsumer.as_asgi())
    # path('ws/mqtt/', MQTTConsumer.as_asgi()),
]