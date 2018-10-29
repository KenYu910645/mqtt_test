#!/usr/bin/env python
import time
import paho.mqtt.client as mqtt
from global_logger import logger
import struct
SERVICE_NAME = "elevator"
#################################3
####  Global helper functions ####
#################################3

######################
#####  Call back #####
######################

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #                  ^^^^^^^^   the private user data as set in Client() or user_data_set()
    print "[on_connect] the private user data as set in Client() or user_data_set() : " , str(userdata) 
    print "[on_connect] response flags sent by the broker : ", flags
    print("[on_connect] the connection result "+ mqtt.connack_string(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("[on_disconnect] Unexpected disconnection.")
    else:
        print "[on_disconnect] Successfully disconnect"

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    print("[on_message] Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))
# client.message_callback_add(sub, callback)
#            callback ref to specify topic name 
# When the message has been sent to the broker an on_publish() callback will be generated.
# client.message_callback_remove(sub)
def on_publish(mosq, obj, mid):
    # This callback is important because even if the publish() call returns success, it does not always mean that the message has been sent.
    # Qos_0 : this simply means that the message has left the client.
    # Qos_1 Qos_2:  this means that the appropriate handshakes have completed.
    pass
# When the broker has acknowledged the subscription, an on_subscribe() callback will be generated.
def on_subscribe(client, userdata, mid, granted_qos):
    print "[on_subscribe] " 
    # The granted_qos variable is a list of integers that give the QoS level the broker has granted for each of the different subscription requests.

# When the broker has acknowledged the unsubscribe, an on_unsubscribe() callback will be generated.
def on_unsubscribe(client, userdata, mid):
    print "[on_unsubscribe] "  

def on_log(client, userdata, level, buf):
    # level == MQTT_LOG_INFO or MQTT_LOG_NOTICE or MQTT_LOG_WARNING, MQTT_LOG_ERR
    # The message itself is in buf
    # print "[on_log] : ", level, "  " , buf
    pass
    
#########################
######    Client ########
#########################
# client = mqtt.Client()
client = mqtt.Client(client_id=SERVICE_NAME, clean_session=True, userdata=None)# , protocol=MQTTv311, transport="tcp")
#       clean_session: If True, the broker will remove all information about this client when it disconnects. 
#                      If False, the client is a durable client and subscription information and queued messages will be retained when the client disconnects.

# client.reinitialise()   
#       takes the same arguments as the Client() constructor.

# client.max_inflight_messages_set(self, inflight) 
#       Defaults to 20. Increasing this value will consume more memory but can increase throughput.

# client.max_queued_messages_set(self, queue_size) 
#       Defaults to 0. 0 means unlimited. When the queue is full, any further outgoing messages would be dropped.

# client.message_retry_set(retry) 
#       Set the time in seconds before a message with QoS>0 is retried, if the broker does not respond.
#       This is set to 5 seconds by default and should not normally need changing
client.enable_logger(logger)

# client.username_pw_set(username, password=None) 
#       Set a username and optionally a password for broker authentication.
client.user_data_set("This is user_data for testing") 
#       Set the private user data that will be passed to callbacks when events are generated. Use this for your own purpose to support your application.
client.will_set(topic=(SERVICE_NAME+"/available"), payload="offline", qos=2, retain=True) 
#       Set a Will to be sent to the broker. If the client disconnects without calling disconnect(), 
#       the broker will publish the message on its behalf.
# client.reconnect_delay_set(min_delay=1, max_delay=120) 
#       The client will automatically retry connection. Between each attempt it will wait a number of seconds between min_delay and max_delay.
#When the connection is lost, initially the reconnection attempt is delayed of min_delay seconds. 

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_unsubscribe = on_unsubscribe
client.on_log = on_log

# client.connect("iot.eclipse.org", 1883, 60)
rc = client.connect(host="iot.eclipse.org", port=1883, keepalive=60, bind_address="")
print "Result of Connection (rc) : ", rc
# keepalive
    # maximum period in seconds allowed between communications with the broker.
    # If no other messages are being exchanged, this controls the rate at which the client will send ping messages to the broker

# bind_address
    # the IP address of a local network interface to bind this client to, assuming multiple interfaces exist

# client.connect_async(host, port=1883, keepalive=60, bind_address="")
        # Use in conjunction with loop_start() to connect in a non-blocking manner. 
        # The connection will not complete until loop_start() is called.

# client.reconnect() 
#       Reconnect to a broker using the previously provided details. 
#       You must have called connect*() before calling this function.

# client.disconnect() 
        # Will not send LW,  
        # Disconnect will not wait for all queued message to be sent, 
        # to ensure all messages are delivered, wait_for_publish() from MQTTMessageInfo should be used. 
        # See publish() for details.

if __name__ == '__main__':

	##########################
	####    Network loop  ####
	##########################


	# client.loop(timeout=1.0, max_packets=1) # Max_packets is obsolute
	#              ^     how long would this function block (timeout Must > KeepAlive)

	# Example : 
	#while True:
	#    client.loop()
	client.loop_start () # Start Network engine at background (free up main thread) 
	# loop_stop (force=False)
	# Blocking call that processes network traffic, dispatches callbacks and
	# handles reconnecting.
	# Other loop*() functions are available that give a threaded interface and a
	# manual interface.
	# client.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)# automatically handles reconnecting. # The timeout and max_packets arguments are obsolete and should be left unset.
	# This is a blocking form of the network loop and will not return until the client calls disconnect(). It automatically handles reconnecting.
	# , use retry_first_connection=True to make it retry the first connection. Warning: This might lead to situations where the client keeps connecting to an non existing host without failing.
	#####################
	#### Subscribing ####
	#####################

	# subscribe(topic, qos=0) # Single topic 
	#client.subscribe([(SERVICE_NAME+"/cmd", 2), (SERVICE_NAME+"/status", 2)]) # Subcribe to multi topic.

	# The function returns a tuple (result, mid), where result is MQTT_ERR_SUCCESS to indicate success or (MQTT_ERR_NO_CONN, None) if the client is not currently connected. mid is the message ID for the subscribe request. The mid value can be used to track the subscribe request by checking against the mid argument in the on_subscribe() callback if it is defined.

	# Raises a ValueError if qos is not 0, 1 or 2, or if topic is None or has zero string length, or if topic is not a string, tuple or list.


	# unsubscribe(topic)   Return same as subscribe

	while True: 
	#####################
	####  PUblishing ####
	#####################
	    # print "[main] loop "
	    client.publish(topic=SERVICE_NAME+"/status", payload="moveing2current", qos=2, retain=False)
		# payload : struct.pack()  
            time.sleep(1)  
	'''

	    rc, the result of the publishing. It could be MQTT_ERR_SUCCESS to indicate success, MQTT_ERR_NO_CONN if the client is not currently connected, or MQTT_ERR_QUEUE_SIZE when max_queued_messages_set is used to indicate that message is neither queued nor sent.
	    mid is the message ID for the publish request. The mid value can be used to track the publish request by checking against the mid argument in the on_publish() callback if it is defined. wait_for_publish may be easier depending on your use-case.
	    wait_for_publish() will block until the message is published. It will raise ValueError if the message is not queued (rc == MQTT_ERR_QUEUE_SIZE).
	    is_published returns True if the message has been published. It will raise ValueError if the message is not queued (rc == MQTT_ERR_QUEUE_SIZE).

	'''






