import paho.mqtt.client as mqtt
import time
import datetime

distance=0

def on_connect(client, userdata, flags, rc):
   global flag_connected
   flag_connected = 1
   client_subscriptions(client)
   print("Connected to MQTT server")

def on_disconnect(client, userdata, rc):
   global flag_connected
   flag_connected = 0
   print("Disconnected from MQTT server")
   
# a callback functions 
def callback_esp32_sensor1(client, userdata, msg):
    global distance
    print('ESP sensor1 data: ', msg.payload.decode('utf-8'))
    distance=int(msg.payload.decode('utf-8'))

def callback_esp32_sensor2(client, userdata, msg):
    print('ESP sensor2 data: ', str(msg.payload.decode('utf-8')))

def callback_rpi_broadcast(client, userdata, msg):
    print('RPi Broadcast message:  ', str(msg.payload.decode('utf-8')))

def client_subscriptions(client):
    client.subscribe("esp32/#")
    client.subscribe("rpi/broadcast")

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,"rpi_client1") #this should be a unique name

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.message_callback_add('esp32/sensor1', callback_esp32_sensor1)
    client.message_callback_add('esp32/sensor2', callback_esp32_sensor2)
    client.message_callback_add('rpi/broadcast', callback_rpi_broadcast)
    client.connect('127.0.0.1',1883)
    # start a new thread
    client.loop_start()
    client_subscriptions(client)
    print("......client setup complete............")

    while True:
        time.sleep(4)   
        if (flag_connected != 1):
            print("flag_connected: ",flag_connected)
            print("trying to connect MQTT server..")
            
if __name__ == "__main__":
    flag_connected = 0
    main()
    
import threading
class sensor_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            print('thread executing')
            main()

        except Exception as e:
            print(e)