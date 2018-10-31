#!/usr/bin/env python
import time
import paho.mqtt.client as mqtt
from global_logger import logger
import struct

IS_PUB_WITHOUT_CONNECT = False



class MQTT_OBJ():
	def __init__(self,client_id="service_provider", broker_ip="iot.eclipse.org", port=1883, keepalive=10, clean_session=True ):
		# -----   Member variable --------#
		self.sub_list = [] # Record topic that subscribe
		self.available = "offline" # "online or offline"
		self.client = mqtt.Client(client_id=client_id, clean_session=clean_session, userdata=None)# , protocol=MQTTv311, transport="tcp")
		self.client.enable_logger(logger)
		# client.user_data_set("This is user_data for testing")
		self.client.will_set(topic=(client_id+"/available"), payload="offline", qos=2, retain=True) 


		self.client.on_connect = self.on_connect
		self.client.on_disconnect = self.on_disconnect
		self.client.on_message = self.on_message
		self.client.on_publish = self.on_publish
		self.client.on_subscribe = self.on_subscribe
		self.client.on_unsubscribe = self.on_unsubscribe
		self.client.on_log = self.on_log

		# client.connect("iot.eclipse.org", 1883, 60)
		# This is a blocking function 
		rc = self.client.connect(host=broker_ip, port=port, keepalive=keepalive, bind_address="")
		logger.info("[Connection] rc = " +  str(rc))

		#-----   Start Mqtt Engine  -----#
		self.client.loop_start ()
		
	def add_subscriber(self, sub_req):
		'''
		Input : sub_req = [("topic1" , qos ) , ("topic2", qos), ....]    
		'''
		for i in sub_req:

			#----------------  Valid check  ----------------# 
			is_valid_subreq = True
			for j in self.sub_list:
				if i[0] == j[0]: # This topic has already been subscribe
					if i[1] != j[1]: # But Qos has change 
						j[1] = i[1] # modified sub_qos as req asked
					else: # Igonre sub_req because this topic has already been sub.
						is_valid_subreq = False
			
			#----------------  Add sub_req to sub_list ------------------# 
			if is_valid_subreq:  # 
				self.sub_list.append(i)
		
		# ---------  real subcribe send to broker ------------#
		self.client.subscribe(self.sub_list)

	def publish (self, topic, payload, qos, retain, timeout = 10):
		# This is a blocking function 
		'''
		wait_for_publish() will block until the message is published. It will raise ValueError if the message is not queued (rc == MQTT_ERR_QUEUE_SIZE).
		is_published returns True if the message has been published. It will raise ValueError if the message is not queued (rc == MQTT_ERR_QUEUE_SIZE).
		Output : 
		    publish result : 
		'''
		pub_rc = self.client.publish(topic, payload, qos, retain)
		logger.info("[publish] " + str(payload) + " to " + topic + " (Q" + str(qos) + ", R" + str(int(retain))+", Mid: " + str(pub_rc[1]) + ")")
		if pub_rc[0] != mqtt.MQTT_ERR_SUCCESS : # Something wrong
			logger.error("[publish]" +  mqtt.error_string(pub_rc[0]) + " (Mid: " + str(pub_rc[1])) # pub_rc=(result,mid)
		
		#---------  wait for published completed --------#  (on_publish will be called first.)
		t_start = time.time()
		while pub_rc.is_published():
			# logger.info( "is_published"  + str(pub_rc.is_published()))
			if time.time() - t_start >= timeout:
				return "GG timeout"
			time.sleep(0.01)
		# pub_rc.wait_for_publish() # Wait until on_publish CB
		logger.info("[publish] Completed  " + ", Mid: " + str(pub_rc[1]) + ")")
		return 

	# The callback for when the client receives a CONNACK response from the server.
	def on_connect(self,client, userdata, flags, rc):
		#                  ^^^^^^^^   the private user data as set in Client() or user_data_set()
		# print "[on_connect] the private user data as set in Client() or user_data_set() : " , str(userdata) 
		# print "[on_connect] response flags sent by the broker : ", flags
		logger.info("[connect_CB] "+ mqtt.connack_string(rc))
		self.available = "online"
		# Subscribing in on_connect() means that if we lose the connection and
		# reconnect then subscriptions will be renewed.
		# client.subscribe("$SYS/#")
		client.subscribe(self.sub_list) # Again all 

	def on_disconnect(self,client, userdata, rc):
		self.available = "offline"
		if rc != 0:
			logger.info("[on_disconnect] Unexpected disconnection.")
		else:
			logger.info("[on_disconnect] Successfully disconnect")

	# The callback for when a PUBLISH message is received from the server.
	def on_message(self,client, userdata, message):
		logger.info("[on_message] Received message '" + str(message.payload) + "' on topic '"
			+ message.topic + "' with QoS " + str(message.qos))
	# client.message_callback_add(sub, callback)
	#            callback ref to specify topic name 
	# When the message has been sent to the broker an on_publish() callback will be generated.
	# client.message_callback_remove(sub)
	def on_publish(self, mosq, obj, mid): # Call be after all of the handshake is completed 
		logger.info("[publish_CB]" + "Complete." + "(Mid: "+ str(mid) + ")")
		# This callback is important because even if the publish() call returns success, it does not always mean that the message has been sent.
		# Qos_0 : this simply means that the message has left the client.
		# Qos_1 Qos_2:  this means that the appropriate handshakes have completed.
	# When the broker has acknowledged the subscription, an on_subscribe() callback will be generated.
	def on_subscribe(self, client, userdata, mid, granted_qos):
		logger.info ("[subscribe_CB] Subscribe AWK."+ "(Mid: "+ str(mid) + ")" )
		# The granted_qos variable is a list of integers that give the QoS level the broker has granted for each of the different subscription requests.

	# When the broker has acknowledged the unsubscribe, an on_unsubscribe() callback will be generated.
	def on_unsubscribe(self, client, userdata, mid):
		logger.info( "[unsubscribe_CB] Unsubscribe AWK"+ "(Mid: "+ str(mid) + ")" )  

	def on_log(self,client, userdata, level, buf):
		# level == MQTT_LOG_INFO or MQTT_LOG_NOTICE or MQTT_LOG_WARNING, MQTT_LOG_ERR
		# The message itself is in buf
		# print "[on_log] : ", level, "  " , buf
		pass
