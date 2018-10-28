import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

def on_disconnect():
    pass
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

#Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")

client = mqtt.Client(client_id="AMR", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
#  If True, the broker will remove all information about this client when it disconnects. If False, the client is a durable client and subscription information and queued messages will be retained when the client disconnects.
# Transport = "tcp"  "websockets"
# protocal  = MQTTv31 or MQTTv311
# client.reinitialise()   takes the same arguments as the Client() constructor.
# client.max_inflight_messages_set(self, inflight) Defaults to 20. Increasing this value will consume more memory but can increase throughput.
# client.max_queued_messages_set(self, queue_size) Defaults to 0. 0 means unlimited. When the queue is full, any further outgoing messages would be dropped.

# client.message_retry_set(retry) # Set the time in seconds before a message with QoS>0 is retried, if the broker does not respond.
# This is set to 5 seconds by default and should not normally need changing
# client.enable_logger(logger=None)
# client.username_pw_set(username, password=None) Set a username and optionally a password for broker authentication.
# client.user_data_set(userdata) Set the private user data that will be passed to callbacks when events are generated. Use this for your own purpose to support your application.
# client.will_set(topic, payload=None, qos=0, retain=False) Set a Will to be sent to the broker. If the client disconnects without calling disconnect(), the broker will publish the message on its behalf.
# client.reconnect_delay_set(min_delay=1, max_delay=120) The client will automatically retry connection. Between each attempt it will wait a number of seconds between min_delay and max_delay.
#When the connection is lost, initially the reconnection attempt is delayed of min_delay seconds. It’s doubled between subsequent attempt up to max_delay.
client.on_connect = on_connect
client.on_message = on_message

# client.connect("iot.eclipse.org", 1883, 60)
client.connect(host="iot.eclipse.org", port=1883, keepalive=60, bind_address="")
# keepalive
    # maximum period in seconds allowed between communications with the broker. If no other messages are being exchanged, this controls the rate at which the client will send ping messages to the broker
# bind_address
    # the IP address of a local network interface to bind this client to, assuming multiple interfaces exist
client.connect_async(host, port=1883, keepalive=60, bind_address="")
# Use in conjunction with loop_start() to connect in a non-blocking manner. The connection will not complete until loop_start() is called.
client.reconnect() # Reconnect to a broker using the previously provided details. You must have called connect*() before calling this function.

client.disconnect() # Will not send LW,  Disconnect will not wait for all queued message to be sent, to ensure all messages are delivered, wait_for_publish() from MQTTMessageInfo should be used. See publish() for details.


##########################
####    Network loop  ####
##########################


# client.loop(timeout=1.0, max_packets=1)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()









