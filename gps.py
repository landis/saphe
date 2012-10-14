#!/usr/bin/python
# Written by James Landritsi http://james.landritsi.com September 2012
# License: GPL 2.0

import os
import time
import threading
from gps import *                                         # GPS
import sqlite3

# ========================
# Switches
# ========================
DEBUG = 1
LOGGER = 0

# ========================
# DB Setup
# ========================
if LOGGER:
  conn = sqlite3.connect('gps.db')
  c = conn.cursor()
  c.execute('''CREATE TABLE gpslog (utc text, lat text, lon text)''')
  conn.commit()
  conn.close()

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd                         # bring it in scope
    gpsd = gps(mode=WATCH_ENABLE)       # starting the stream of info
    self.current_value = None
    self.running = True                 # setting the thread running to true
    
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next()                       # this will continue to loop and grab EACH set of gpsd info to clear the buffer

if __name__ == '__main__':
  gpsp = GpsPoller()                    # create the thread
  try:
    gpsp.start()                        # start it up
    while True:
      if DEBUG:
        print
        print ' GPS reading'
        print '----------------------------------------'
        print 'latitude    ' , gpsd.fix.latitude
        print 'longitude   ' , gpsd.fix.longitude
        print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
        print 'altitude (m)' , gpsd.fix.altitude
        print 'eps         ' , gpsd.fix.eps
        print 'epx         ' , gpsd.fix.epx
        print 'epv         ' , gpsd.fix.epv
        print 'ept         ' , gpsd.fix.ept
        print 'speed (m/s) ' , gpsd.fix.speed
        print 'climb       ' , gpsd.fix.climb
        print 'track       ' , gpsd.fix.track
        print 'mode        ' , gpsd.fix.mode
        print
        print 'sats        ' , gpsd.satellites

      if LOGGER:
        tmsp = gpsd.utc,'+',gpsd.fix.time
        gps_tuple = (tmsp,gpsd.fix.latitude,gpsd.fix.longitude)
        c.execute('INSERT INTO gpslog VALUES (?,?,?)', (gps_tuple))
        conn.commit()
        conn.close()
        
      time.sleep(5)

    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
      print "\nKilling Thread..."
      gpsp.running = False
      gpsp.join() # wait for the thread to finish what it's doing
    print "Done.\nExiting."
