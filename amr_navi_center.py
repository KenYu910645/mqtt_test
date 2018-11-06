#!/usr/bin/env python
import time
import paho.mqtt.client as mqtt
from global_logger import logger
import json
from MQTT.mqtt_template import MQTT_OBJ

CLIENT_NAME = "AMR_4" # Tow different mqtt client MUST have different name, and '#' , '+' , '/' is NOT allow in topic name
is_tc_available = ""

############################
###  CallBack functions  ###
############################

def path_allowed_CB(client, userdata, message):
	logger.info("[MQTT] path_allowed_CB :  " + str(message.payload) + "(Q" + str(message.qos) + ", R" + str(message.retain) + ")")
	# TODO 

def traffic_controller_available_CB(client, userdata, message):
	global is_tc_available
	logger.info("[MQTT] traffic_controller_available_CB :  " + str(message.payload) + "(Q" + str(message.qos) + ", R" + str(message.retain) + ")")
	is_tc_available = message.payload


if __name__ == '__main__':
	#########################
	###  MQTT Connection  ###
	#########################
	'''
	Init MQTT_OBJ will automative connect to broker and start a background thread for mqtt network
	client_id , broker_ip , logger  : should be setup right.
        logger is a python logging handle, if you don't want to use it , pass None . (logger = None)
	'''
	mqtt_obj = MQTT_OBJ(client_id=CLIENT_NAME, broker_ip="iot.eclipse.org", port=1883, keepalive=10, clean_session=True, logger = logger)
	# Wait for connection Accpeted by broker (Optional) 
	while mqtt_obj.available != "online":
		time.sleep(0.1)
	#########################
	###      Subcriber    ###
	#########################
	'''
	Add your subcribe topic  in this function  [ (topic1, qos,  Callback_fun1),  (topic2, qos, Callback_fun2), (...) , .... ]
	'''
	mqtt_obj.add_subscriber([ (CLIENT_NAME+"/path_allowed", 2, path_allowed_CB)  , ("traffic_controller/available", 1, traffic_controller_available_CB)])

	while True:
		# --------- Check Mqtt Connection ---------# 
		# User should always check current connection status, before publishing any message.
		if mqtt_obj.available == "offline":
			logger.warn("[MQTT] No Mqtt Connection")
			# TODO 
		else: # Online
			##################################################
			###  Publish something don't need to track   #####
			##################################################
			# Non-blocking publish , suitable for qos0.
			mqtt_obj.publish(topic = CLIENT_NAME+"/position", payload = "432", qos = 1, retain = False)
			#### Blocking publish
			# mqtt_obj.publish_blocking(topic = "elevator/status", payload = "test test test ", qos = 1, retain = False, timeout = 10)
			
			#############################
			###  Publish with track   ###
			#############################
			# Using publish result to track publish handshake is completed or not .
			if is_tc_available == "online" and mqtt_obj.available == "online": 
				rc = mqtt_obj.publish(topic = CLIENT_NAME+"/path_req", payload = "[432, 431, 430, EV4W, EV_IN]", qos = 2, retain = False)
				if rc == None: 
					# Didn't publish because client is current offline
					# TODO 
					pass
				else: 
					if rc.is_published(): # == True , Finish all handshake with broker (qos1, qos2)
						# TODO 
						pass
					else: 
						pass
			else: 
				logger.warn("[MQTT] One of the client is not online.")
		time.sleep(3)
