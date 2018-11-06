#!/usr/bin/env python
import time
import paho.mqtt.client as mqtt
from global_logger import logger
import json
from MQTT.mqtt_template import MQTT_OBJ

CLIENT_NAME = "traffic_controller" # Tow different mqtt client MUST have different name, and '#' , '+' , '/' is NOT allow in topic name
amr_name_list = ["AMR_4", "AMR_5"]
is_amr_available = ""
############################
###  CallBack functions  ###
############################

def path_req_CB(client, userdata, message):
	# logger.info("+++++++++++++++++++++  THis is Self define CB")
	logger.info("[path_req_CB] Received message '" + str(message.payload) + "' on topic '"
	+ message.topic + "' with QoS " + str(message.qos))

def amr_available_CB(client, userdata, message):
	global is_amr_available
	is_amr_available = message.payload

if __name__ == '__main__':

	#########################
	###  MQTT Connection  ###
	#########################
	# Init MQTT_OBJ will automative connect to broker and start a background thread for mqtt network
	mqtt_obj = MQTT_OBJ(client_id=CLIENT_NAME, broker_ip="iot.eclipse.org", port=1883, keepalive=10, clean_session=True, logger = logger)

	#########################
	###      Subcriber    ###
	#########################
	mqtt_obj.add_subscriber([("+/path_req", 2, path_req_CB)  , (amr_name_list[0]+"/available", 2, amr_available_CB)])
	#                       [ (topic1, qos,  Callback_fun1),  (topic2, qos, Callback_fun2), (...) , .... ]       	
	while True:
		
		# --------- Check Mqtt Connection ---------# 
		if mqtt_obj.available == "offline":
			logger.warn("[NetWork] No Mqtt Connection")
		else: # online 
			#### Blocking publish
			# mqtt_obj.publish_blocking(topic = "elevator/status", payload = "test test tes ", qos = 1, retain = False, timeout = 10)
			##################################################
			###  Publish something don't need to track   #####
			##################################################
			# mqtt_obj.publish(topic = CLIENT_NAME+"/position", payload = "432", qos = 1, retain = False)

			###############################
			###  Publish with track   #####
			###############################
			if is_amr_available == "online" and mqtt_obj.available == "online":
				rc = mqtt_obj.publish(topic = amr_name_list[0]+"/path_allowed", payload = "[432, 431, 430, EV4W, EV_IN]", qos = 2, retain = False)
				if rc == None: 
					# Didn't publish because client is current offline
					# TODO 
					pass
				else: 
					if rc.is_published(): # == True , when get PUB_AWK from broker (qos1, qos2)
						# TODO 
						pass
			else: 
				logger.warn("[NetWork] One of the client is not online.")

		time.sleep(3)
