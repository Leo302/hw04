import paho.mqtt.client as paho
import string as string1
import locale
import matplotlib.pyplot as plt
import numpy as np
import serial
import time

# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client
# MQTT broker hosted on local machine
mqttc = paho.Client()
# Settings for connection
# TODO: revise host to your ip
host = "192.168.137.10" 
topic= "Mbed"

x = []
y = []
z = []
sample_time=[]

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    global x
    global y
    global z
    global start
    global sample_time
    print("[Received] Topic: " + msg.topic + ", Message: " + msg.payload.decode("UTF-8") + "\n")
    x.append(locale.atof(msg.payload[0:6].decode("UTF-8")))
    y.append(locale.atof(msg.payload[7:13].decode("UTF-8")))
    z.append(locale.atof(msg.payload[14:20].decode("UTF-8")))
    y_time=time.time()
    sample_time.append(y_time-start)

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

def store_x(x,msg):
    x.append(string1.atof(str(msg.payload[0:7])))
    print(x+"\n")
    return x    

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe
#mqttc.store_x = store_x

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

start=time.time()
mqttc.loop_start()
tend=time.time()
while tend-start<=20:
    tend=time.time()
    mqttc.loop_stop()
    fig, ax = plt.subplots(1, 1)
    l1,=ax.plot(sample_time,x)
    l2,=ax.plot(sample_time,y)
    l3,=ax.plot(sample_time,z)
    ax.set_xlabel('timestamp')
    ax.set_ylabel('acc value')
    sax.legend((l1,l2,l3),('X','Y','Z'))
    plt.show()
    s.close()
