#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
Publish some messages to queue
"""
import paho.mqtt.publish as publish


msgs = [{'topic': "kids/yolo", 'payload': "jump"},
        {'topic': "adult/pics", 'payload': "some photo"},
        {'topic': "adult/news", 'payload': "extra extra"},
        {'topic': "adult/news", 'payload': "super extra"}]

host = "localhost"


if __name__ == '__main__':
    # publish a single message
    print publish.single(topic="test", payload="call to 1F", hostname='192.168.1.102', qos=1)
    
    # publish multiple messages
    #publish.multiple(msgs, hostname=host)


# vi: set fileencoding=utf-8 :
