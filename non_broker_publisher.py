#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
Publish some messages to queue
"""
import paho.mqtt.publish as publish
import paho.mqtt.client as paho
import json

msgs = {'content': "release_test", 'robot_id': "AMR250 # 2"}

host = "localhost"
def on_publish(mosq, obj, mid):
    pass


if __name__ == '__main__':
    #client = paho.Client()
    #client.on_publish = on_publish
    # client.connect("192.168.30.67", 1883, 60)
    # publish a single message
    publish.single(topic="amr/status", payload=json.dumps(msgs), hostname='iot.eclipse.org')
    
    # publish multiple messages
    #publish.multiple(msgs, hostname=host)


# vi: set fileencoding=utf-8 :
