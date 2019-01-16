#!/usr/bin/env python

import time
import signal
from pydispatch import dispatcher
#from webserver import WebServer
#from wifimanager import WifiManager

class MVILamp():
	def __init__(self):
		print "HI!"
		signal.signal(signal.SIGINT, self.signal_handler)
		
		#self.wifiManager = WifiManager()
		#self.webServer = WebServer()
		
		#self.setDispatchEvents()

		#self.wifiManager.startAccessPoint()
		#self.webServer.start(False,self.wifiManager.getSSID())

		while True:
			time.sleep(0.5)

	#def setDispatchEvents(self):
	
	def signal_handler(self, signal, frame):
		#self.wifiManager.stopAccessPoint()
		#self.webServer.shutdown()
		sys.exit(0)

if __name__ == "__main__":
	app = MVILamp()