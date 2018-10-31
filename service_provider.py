#!/usr/bin/env python
import time
import paho.mqtt.client as mqtt
from global_logger import logger
import struct
from mqtt_template import MQTT_OBJ
SERVICE_NAME = "service_provider"


# def elevator_state_CB():


if __name__ == '__main__':
	# Init this obj will automative connect to broker and start a background thread for mqtt network
	mqtt_obj = MQTT_OBJ(client_id=SERVICE_NAME, broker_ip="iot.eclipse.org", port=1883, keepalive=10, clean_session=True)
	mqtt_obj.add_subscriber([("elevator/status", 1), ("door/status", 0)])
	while True:
		mqtt_obj.publish("elevator/status", "test test tes ", 1, False)
		time.sleep(3)
