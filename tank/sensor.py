import paho.mqtt.client as mqtt
import time
import datetime

from .models import Tank,SensorData

import smtplib
from email.message import EmailMessage

import RPi.GPIO as GPIO
import time,os

# import datetime

flag_connected = 0
VALVE=16

GPIO.setmode(GPIO.BCM)
GPIO.setup(VALVE,GPIO.OUT)
GPIO.output(VALVE, False)

tank_status='none'

FILL=False
distance=0

def email_alert(subject, body, to):
    tank = Tank.objects.get(name='Prototype')
    
    msg=EmailMessage()
    msg.set_content(body)
    msg['subject']=subject
    msg['to']=to
    msg['from']=f"{tank.name} Tank"

    user='***'
    password='***'

    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()



def add_sensor_data(tank_name, sensor_value, status):
    # Get the tank object
    tank = Tank.objects.get(name=tank_name)
    
    # Create a new SensorData instance
    sensor_data = SensorData(tank=tank, value=sensor_value, tank_status=status)
    
    # Save the SensorData instance
    sensor_data.save()


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
        
    tank=Tank.objects.get(name='Prototype')
    # print(tank.height)
    
    global FILL
    global tank_status
    # print(distance)
    empty=tank.height-tank.upper_limit
    to_fill=tank.height-tank.lower_threshold
    print(tank.height-distance)
    # print("tank.height",tank.height)
    # print("tank.upper_limit",tank.upper_limit)
    # print("tank.lower_threshold",tank.lower_threshold)
        
    # print("empty",empty,"to_fill",to_fill)
    
    if distance<=empty:
        tank_status='Full'
        if FILL!=False:
            FILL=False
            print("Tank Full, Valve Closed")        
            GPIO.output(VALVE, False)
            email_alert("Tank Status", "Tank is filled", "crce.9494.ecs@gmail.com")
            # email_alert("Tank Status", "Tank is filled", "crce.9480.ecs@gmail.com")
            # email_alert("Tank Status", "Tank is filled", "bhoir@fragnel.edu.in")
        add_sensor_data(tank.name, (tank.height-distance), 'Full')
        # global tank_status
        
                        
    elif distance>=to_fill:
        tank_status='Filling'
        if FILL!=True:
            FILL=True
            print("Filling Water, Valve Opened")
            GPIO.output(VALVE, True)
            email_alert("Tank Status", "Tank is filling", "@abc.com")
            # email_alert("Tank Status", "Tank is filling", "@gmail.com")
            # email_alert("Tank Status", "Tank is filling", "@xyz.com")
        add_sensor_data(tank.name, (tank.height-distance), 'Filling')
        # global tank_status
            
    else:
        add_sensor_data(tank.name, (tank.height-distance), 'Neutral')
        # global tank_status
        tank_status='Neutral'
            

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
            # add_sensor_data('Prototype',29)
            main()

        except Exception as e:
            print(e)
