#!/usr/bin/python

import sys
import time
import datetime
import pymetar
import eeml
from Adafruit.BMP085.Adafruit_BMP085 import BMP085

# ========================
# Sensor declare
# ========================
bmp = BMP085(0x77, 3) # ULTRAHIRES Mode
DEBUG = 1

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
# COSM declare
# ========================
LOGGER = 1
API_KEY = '1nmfR0zAp8X0jB27soRr6qCxk_iSAKx5NUJHNGJYajZobz0g'
FEED = 79880
API_URL = '/v2/feeds/{feednum}.xml' .format(feednum = FEED)

# ========================
# Setup
# ========================

#header="Timestamp,KPNE Sealevel Pressure (hPa),Pressure (hPa),Celsius,Fahrenheit,Altitude (m)"
#print header

while (True):
  if pr.getPressure() is not None:
    locAS = pr.getPressure()

  locASP = locAS * 100  
  tmstp = time.strftime("%Y/%m/%d %H:%M:%S")
  temp = bmp.readTemperature()
  tempF = temp * 9 / 5 + 32
  pressure = bmp.readPressure()
  altitude = bmp.readAltitude()
  absaltft = altitude * 3.28084
  pressInHG = pressure / 3386.38816
  altmod = 44330 * (1.0 - pow(pressure/locASP,0.1903))
  altmet = round(altmod, 2)

  if DEBUG:
    lineA = tmstp + "," + str(round(locAS,2)) + "," + str(pressure/100.0) + "," + str(temp) + "," + str(tempF) + "," + str(altmod)
    print lineA
  
  if LOGGER:
    pac = eeml.Pachube(API_URL, API_KEY)
    pac.update([eeml.Data(0, temp, unit=eeml.Celsius())])
    pac.update([eeml.Data(1, tempF, unit=eeml.Fahrenheit())])
    pac.update([eeml.Data(2, pressure)])
    pac.update([eeml.Data(3, altmet)])
    pac.put()
  
  time.sleep(10)
