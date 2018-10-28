#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A small example subscriber
"""
import paho.mqtt.client as paho
import json

def on_message(mosq, obj, msg):
    print "%-20s %d %s" % (msg.topic, msg.qos, msg.payload)
    mosq.publish('pong', 'ack', 0)

def test_callback(mosq, obg, msg):
    print "%-20s %d %s" % (msg.topic, msg.qos, msg.payload)
    print "This is Test callback"
    # print json.loads(msg.payload)['content']
    # mosq.publish('pong', 'ack', 0)


def on_publish(mosq, obj, mid):
    pass

if __name__ == '__main__':
    client = paho.Client(client_id="elevator_server")
    client.on_message = on_message
    client.on_publish = on_publish
    client.will_set(topic = "status", payload="elevator_server is died ", qos=2, retain=False)
    #client.tls_set('root.ca', certfile='c1.crt', keyfile='c1.key')
    #The connect() function connects the client to a broker. This is a blocking function. It takes the following arguments:
    try:
        client.connect("192.168.30.62", 1883, 60) # This is a blocking function 
    except: 
        print "bad"
    client.message_callback_add('test', test_callback)
    client.subscribe("test"    , 2)
    client.subscribe("AMR_2_EV", 0)
    #client.subscribe("$SYS/broker/messages/#", 0)

    while client.loop() == 0:
        pass

# vi: set fileencoding=utf-8 :
