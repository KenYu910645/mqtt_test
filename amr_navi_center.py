#!/usr/bin/env python
import time
import paho.mqtt.client as mqtt
from global_logger import logger
import json
from mqtt_template import MQTT_OBJ

CLIENT_NAME = "AMR_4" # Tow different mqtt client MUST have different name, and '#' , '+' , '/' is NOT allow in topic name
is_tc_available = ""

############################
###  CallBack functions  ###
############################

def path_allowed_CB(client, userdata, message):
	# logger.info("+++++++++++++++++++++  THis is Self define CB")
	logger.info("[path_allowed_CB] Received message '" + str(message.payload) + "' on topic '"
	+ message.topic + "' with QoS " + str(message.qos))

def traffic_controller_available_CB(client, userdata, message):
	global is_tc_available
	is_tc_available = message.payload


if __name__ == '__main__':

	#########################
	###  MQTT Connection  ###
	#########################
	# Init MQTT_OBJ will automative connect to broker and start a background thread for mqtt network
	mqtt_obj = MQTT_OBJ(client_id=CLIENT_NAME, broker_ip="iot.eclipse.org", port=1883, keepalive=10, clean_session=True, logger = logger)

	#########################
	###      Subcriber    ###
	#########################
	mqtt_obj.add_subscriber([ (CLIENT_NAME+"/path_allowed", 2, path_allowed_CB)  , ("traffic_controller/available", 1, traffic_controller_available_CB)])
	#                       [ (topic1, qos,  Callback_fun1),  (topic2, qos, Callback_fun2), (...) , .... ]       	
	while True:
		
		# --------- Check Mqtt Connection ---------# 
		if mqtt_obj.available == "offline":
			logger.warn("[NetWork] No Mqtt Connection")
		
		#### Blocking publish
		# mqtt_obj.publish_blocking(topic = "elevator/status", payload = "test test tes ", qos = 1, retain = False, timeout = 10)
		##################################################
		###  Publish something don't need to track   #####
		##################################################
		mqtt_obj.publish(topic = CLIENT_NAME+"/position", payload = "432", qos = 1, retain = False)

		###############################
		###  Publish with track   #####
		###############################
		if is_tc_available == "online" and mqtt_obj.available == "online":
			rc = mqtt_obj.publish(topic = CLIENT_NAME+"/path_req", payload = "[432, 431, 430, EV4W, EV_IN]", qos = 2, retain = False)
			if rc == None: 
				# Didn't publish because client is current offline
				# TODO 
				pass
			else: 
				if rc.is_published(): # == True , when get PUB_AWK from broker (qos1, qos2)
					# TODO 
					pass
		else: 
			logger.warn("[NetWork] Traffic controller is offline")

		time.sleep(3)
