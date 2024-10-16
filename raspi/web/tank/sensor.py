import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import time, json
import datetime

from .models import Tank,SensorData

import smtplib
from email.message import EmailMessage

import RPi.GPIO as GPIO
import time,os

# import datetime

flag_connected = 0
status="none"

tank_status=old_ts=2
water_level=0

# FILL=False
# distance=0

def email_alert(subject, body, to):
    tank = Tank.objects.get(name='Prototype')
    
    msg=EmailMessage()
    msg.set_content(body)
    msg['subject']=subject
    msg['to']=to
    msg['from']=f"{tank.name} Tank"

    # user='email_id@gmail.com'
    # password='app password'

    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

def on_subscribe(client, userdata, mid, reason_code_list, properties):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")

def status_decoder(value):
    cases = {
        0: "Neutral",
        1: 'Filling',
        2: 'Full'
    }
    return cases.get(value)

def on_message(client, userdata, message):
    global water_level, tank_status, old_ts, status
    tank=Tank.objects.get(name='Prototype')
    # print("%s %s" %(message.topic, message.payload.decode("utf-8")))
    msg=message.payload.decode("utf-8")
    if(message.topic=="esp32/tank"):
        tank_json_object = json.loads(msg)
        water_level=tank_json_object['wl']
        tank_status=tank_json_object['ts']
        # print("wl= ",tank_json_object['wl'])
        # print("ts= ",tank_json_object['ts'])
        status=status_decoder(int(tank_status))
        add_sensor_data(tank.name, water_level, status)
    
    if old_ts!=tank_status and tank_status!=0:
        old_ts=tank_status
        print("send email")
        
    
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe("esp32/#")

def add_sensor_data(tank_name, sensor_value, status):
    # Get the tank object
    tank = Tank.objects.get(name=tank_name)
    
    # Create a new SensorData instance
    sensor_data = SensorData(tank=tank, value=sensor_value, tank_status=status)
    
    # Save the SensorData instance
    sensor_data.save()
   
# a callback functions 
def callback_esp32_sensor1(client, userdata, msg):
    global distance
    print('ESP sensor1 data: ', msg.payload.decode('utf-8'))
    distance=int(msg.payload.decode('utf-8'))
        
    tank=Tank.objects.get(name='Prototype')
    # print(tank.height)
    
    global FILL
    global tank_status
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
            email_alert("Tank Status", "Tank is filling", "crce.9494.ecs@gmail.com")
            # email_alert("Tank Status", "Tank is filling", "crce.9480.ecs@gmail.com")
            # email_alert("Tank Status", "Tank is filling", "bhoir@fragnel.edu.in")
        add_sensor_data(tank.name, (tank.height-distance), 'Filling')
        # global tank_status
            
    else:
        add_sensor_data(tank.name, (tank.height-distance), 'Neutral')
        # global tank_status
        tank_status='Neutral'
            
# def client_subscriptions(client):
#     client.subscribe("esp32/#")
#     client.subscribe("rpi/broadcast")

def main():    
    # client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,"rpi_client1") #this should be a unique name

    # client.on_connect = on_connect
    # client.on_disconnect = on_disconnect
    # client.message_callback_add('esp32/sensor1', callback_esp32_sensor1)
    # client.message_callback_add('esp32/sensor2', callback_esp32_sensor2)
    # client.message_callback_add('rpi/broadcast', callback_rpi_broadcast)
    # client.connect('127.0.0.1',1883)
    # # start a new thread
    # client.loop_start()
    # client_subscriptions(client)
    # print("......client setup complete............")

    # while True:
    #     time.sleep(4)   
    #     if (flag_connected != 1):
    #         print("flag_connected: ",flag_connected)
    #         print("trying to connect MQTT server..")
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    mqttc.on_connect = on_connect
    # mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe
    # mqttc.on_unsubscribe = on_unsubscribe

    # mqttc.user_data_set([])
    mqttc.connect("127.0.0.1",1883)

    # subscribe.callback(on_message, "esp32/#", hostname="127.0.0.1", port=1883) #, userdata={"message_count": 0})

    mqttc.message_callback_add("esp32/#", on_message)
    mqttc.loop_start()

    print("after callback")


            
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