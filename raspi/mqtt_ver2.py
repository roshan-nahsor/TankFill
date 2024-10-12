import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import time, json

def on_subscribe(client, userdata, mid, reason_code_list, properties):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")

# def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
#     # Be careful, the reason_code_list is only present in MQTTv5.
#     # In MQTTv3 it will always be empty
#     if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
#         print("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
#     else:
#         print(f"Broker replied with failure: {reason_code_list[0]}")
#     client.disconnect()

# def on_message(client, userdata, message):
    # # userdata is the structure we choose to provide, here it's a list()
    # userdata.append(message.payload)
    # # We only want to process 10 messages
    # if len(userdata) >= 10:
    #     client.unsubscribe("$SYS/#")
    # print(client, message.payload)

def on_message(client, userdata, message):
    print("%s %s" %(message.topic, message.payload.decode("utf-8")))
    # userdata["message_count"] += 1
    # if userdata["message_count"] >= 5:
    #     # it's possible to stop the program by disconnecting
    #     client.disconnect()
    
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe("esp32/#")

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

# print(f"Received the following message: {mqttc.user_data_get()}")
data = {
    "sensor_id": 1,
    "temperature": 25.6,
    "humidity": 60
}

# Convert the data to JSON format
json_data = json.dumps(data)

while True:
    time.sleep(5)
    # publish.single("rpi/broadcast", "payload", hostname="127.0.0.1", port=1883)
    publish.single("rpi/broadcast", json_data, hostname="127.0.0.1", port=1883)