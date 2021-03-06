#!/usr/bin/python
# Written by James Landritsi http://james.landritsi.com September 2012
# License: GPL 2.0

import sys
import os
import time
import datetime
import threading
#import eeml                                               # COSM
import pymetar                                            # BMP085
from Adafruit.BMP085.Adafruit_BMP085 import BMP085        # BMP085
from gps import *                                         # GPS

# ========================
# Switches
# ========================
t1 = os.getpid()
DEBUG = 1
LOGGER = 0

# ========================
# Metar declare
# ========================
station = "KPNE"
rf=pymetar.ReportFetcher(station)
rep=rf.FetchReport()
rp=pymetar.ReportParser()
pr=rp.ParseReport(rep)
locAS = 1013.25

# ========================
# COSM variables
# ========================
#API_KEY = '1nmfR0zAp8X0jB27soRr6qCxk_iSAKx5NUJHNGJYajZobz0g'
#FEED = 79880
#API_URL = '/v2/feeds/{feednum}.xml' .format(feednum = FEED)

# ========================
# Setup
# ========================

class BmpPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global bmp
    bmp = BMP085(0x77, 3) # ULTRAHIRES Mode
    self.current_value = None
    self.running = True
    
  def run(self):
    global bmp
        
if __name__ == '__main__':
  bmpp = BmpPoller()
  bmpp.start()
  
  while True:
    try:
      temp = bmp.readTemperature()
      pressure = bmp.readPressure()
      altitude = bmp.readAltitude()
      if pr.getPressure() is not None:
        locAS = pr.getPressure()
      
      locASP = locAS * 100
      tmstp = time.strftime("%Y/%m/%d %H:%M:%S")
      tempF = temp * 9 / 5 + 32
      absaltft = altitude * 3.28084
      pressInHG = pressure / 3386.38816
      altmod = 44330 * (1.0 - pow(pressure/locASP,0.1903))
      altmet = round(altmod, 2)
      
      if DEBUG:
        lineA = tmstp + "," + str(round(locAS,2)) + "," + str(pressure/100.0) + "," + str(temp) + "," + str(tempF) + "," + str(altmod)
        print lineA
  
#      if LOGGER:
#        pac = eeml.Pachube(API_URL, API_KEY)
#        pac.update([eeml.Data(0, temp, unit=eeml.Celsius())])
#        pac.update([eeml.Data(1, tempF, unit=eeml.Fahrenheit())])
#        pac.update([eeml.Data(2, pressure)])
#        pac.update([eeml.Data(3, altmet)])
#        pac.put()
        
      time.sleep(5)

    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
      print "\nKilling Thread..."
      os.popen("kill -9 "+str(t1))
