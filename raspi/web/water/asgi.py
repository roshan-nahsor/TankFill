"""
ASGI config for water project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from tank.routing import ws_urlpatterns

# from tank.consumers import MyMqttConsumer                                  #mqttagi

# from mqttasgi import MQTTProtocol


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'water.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns)),
})




# 'mqtt': MyMqttConsumer.as_asgi(),                                       #mqttasgi
    # 'http': django_asgi_app(),
    #chatGPT
    # 'mqtt': MQTTProtocol(
    #     'mqtt://127.0.0.1:1883',
    #     'raspi',
    #     ['esp32/sensor1', 'topic2'],
    #     debug=True,
    # ),