#!/usr/bin/python

import enum
import logging
import paho.mqtt.client as mqtt
import time

log = logging.getLogger('jenkins_indicator')

rc_messages = {
"0": "Connection successful",
"1": "Connection refused incorrect protocol version",
"2": "Connection refused invalid client identifier",
"3": "Connection refused server unavailable",
"4": "Connection refused bad username or password",
"5": "Connection refused not authorised"
}
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    print (rc_messages[str(rc)])

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    pass


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)

class State(enum.IntEnum):
    Off = 0
    Succeeded = 1
    Failed = 2
    InProgressLastSucceeded = 3
    InProgressLastFailed = 4


class MQTTBroadcast():
    def __init__(self, mqtt_broker):
        self.mqtt_broker = mqtt_broker
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = on_message
        self.mqttc.on_connect = on_connect
        self.mqttc.on_publish = on_publish
        self.mqttc.on_subscribe = on_subscribe
        # Uncomment to enable debug messages
        # mqttc.on_log = on_log
        self.mqttc.username_pw_set(username=mqtt_broker.username, password=mqtt_broker.password)
        


    def send_project_info(self, topic, indicator_status):
        self.mqttc.connect(self.mqtt_broker.address, self.mqtt_broker.port, 60)
        self.mqttc.loop_start()
        self.topic = topic

        print("topic: " + self.topic)
        print("class")
        infot = self.mqttc.publish(topic, '{"gpio":{"status":' + '"' +indicator_status + '"' +'}}', qos=2)

        infot.wait_for_publish()
        if infot.is_published():
           print ("published succesful")
        else:
           print ("Failed to publish")
        time.sleep(4) # wait
        self.mqttc.loop_stop() #stop the loop
        self.mqttc.disconnect()
