import json
from asyncio import sleep
from random import randint

from . import sensor
# sensor.main()
sensor.sensor_thread().start()
# print(sensor.distance)
from channels.generic.websocket import AsyncWebsocketConsumer

class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # while True:
        #     await self.send(json.dumps({'value': sensor.water_level,'status': sensor.status}))
        #     await sleep(5)
        
    # --------------------websocket disconnect--------------------
        try:
            while True:
                # Send sensor data
                await self.send(json.dumps({
                    'value': sensor.water_level,
                    'status': sensor.status
                }))
                await sleep(5)
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            await self.close()

    async def disconnect(self, close_code):
        # Any additional cleanup can go here
        pass
    # --------------------websocket disconnect--------------------




# ===========Valeron (Claudy)
# import json
# import paho.mqtt.client as mqtt
# from channels.generic.websocket import AsyncWebsocketConsumer
 
# # MQTT broker URL
# # BROKER_URL = 'mqtt://your-mqtt-broker-url:port'
 
# class GraphConsumer(AsyncWebsocketConsumer):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,"rpi_client1")
    #     self.mqtt_client.on_connect = self.on_connect
    #     self.mqtt_client.on_message = self.on_message
 
    # async def connect(self):
    #     await self.accept()
    #     self.mqtt_client.connect('127.0.0.1',1883)
    #     self.mqtt_client.loop_start()
 
    # async def on_connect(self, client, userdata, flags, rc):
    #     print('Connected to MQTT broker with result code:', rc)
    #     client.subscribe('esp32/sensor1')
 
    # async def on_message(self, client, userdata, msg):
    #     payload = msg.payload.decode('utf-8')
    #     await self.send(text_data=json.dumps({'value': payload}))
 
    # async def disconnect(self, close_code):
    #     self.mqtt_client.loop_stop()
    #     self.mqtt_client.disconnect()
 
    # async def receive(self, text_data):
    #     await self.connect()
 
    # async def websocket_connect(self, event):
    #     print('WebSocket connected')
    #     await self.send(text_data=json.dumps({'status': 'connected'}))
 
    # async def websocket_disconnect(self, event):
    #     print('WebSocket disconnected')
    #     await self.disconnect(event.code)

# class GraphConsumer(AsyncWebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.distance = 0  # Initialize distance to 0

#     async def connect(self):
#         await self.accept()
        
#         while True:
#             await self.send(json.dumps({'value': self.distance}))
#             await asyncio.sleep(1)  # Use asyncio.sleep instead of sleep


# class GraphConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
        
#         for i in range(1000):
#             await self.send(json.dumps({'value': randint(-20, 20)}))
#             await sleep(1)

# ===========Technology for Noobs https://www.youtube.com/watch?v=32iJlPDNLQY

    # async def disconnect(self,close_code):
    #     pass
    #     await self.disconnect

#-----------found on some forum
    # async def websocket_disconnect(self, event):
    #     # Leave room group
    #     await self.channel_layer.group_discard(
    #         self.room_name,
    #         self.channel_name
    #     )
    #     raise StopConsumer()
    # pass



#=============mqttasgi
# from mqttasgi.consumers import MqttConsumer
# class MyMqttConsumer(MqttConsumer):
    # async def connect(self):
    #     await self.subscribe('esp32/sensor1', 2)
    #     # await self.channel_layer.group_add("my.group", self.channel_name)
    # async def receive(self, mqtt_message):
    #     print('Received a message at topic:', mqtt_message['topic'])
    #     print('With payload', mqtt_message['payload'])
    #     print('And QOS:', mqtt_message['qos'])
    #     pass
    # async def my_custom_message(self, event):
    #     print('Received a channel layer message')
    #     print(event)
    # async def disconnect(self):
    #     await self.unsubscribe('my/testing/topic')

#chatGPT
# from channels.generic.websocket import AsyncJsonWebsocketConsumer
# class MQTTConsumer(AsyncJsonWebsocketConsumer):
    # async def connect(self):
    #     await self.accept()

    # async def mqtt_message(self, event):
    #     message = event['message']
    #     await self.send_json(message)
