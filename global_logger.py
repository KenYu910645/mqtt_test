import logging 

# logger
# Set up logger
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger('cherrypy')
logger.setLevel(logging.DEBUG)

# Print out logging message on console
h_console = logging.StreamHandler()
h_console.setFormatter(formatter)
h_console.setLevel(logging.DEBUG)
logger.addHandler(h_console)

# Record logging message at logging file
h_file = logging.FileHandler("mqtt.log")
h_file.setFormatter(formatter)
h_file.setLevel(logging.DEBUG)
logger.addHandler(h_file)
