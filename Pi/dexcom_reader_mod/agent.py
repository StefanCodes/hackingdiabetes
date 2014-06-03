
import xml.etree.ElementTree as ET
import time
import requests
import datetime
import calendar
import sys
from readdata import Dexcom
from filesender import senddata


#Usage: py agent.py sourceFile offsetMins
if __name__ == '__main__':
    while 1:
        #Parameter parsing
        if (len(sys.argv) != 3):
            print "Usage: python agent.py sourceFile offsetMins"
            print "   sourceFile is the name of the local xml file to read"
            print "   offsetMins is the number of minutes to subtract from the last sync time"
            print ""
            print "For live data polled from a Dexcom, use live.xml"
            print "offsetMins of -1 will fetch *all* available data"
            print "offsetMins of 10 will fetch all data since the last fetch, less 10 minutes"
            exit()

        # Error handling goes here. Heh.

        filename = sys.argv[1]
        offsetMins = int(sys.argv[2])

        lastTime = 0
        try:
            f = open('last-time.txt', 'r+')
            lastTime = int(f.readline())
            f.close()
        except:
            pass #do nothing

        if (lastTime > 0):
            start_date = datetime.datetime.fromtimestamp(lastTime)
        else:
            start_date = datetime.datetime.min;

        # A value of 10 means that data will be grabbed since 10 minutes before lastTime
        if (offsetMins >= 0 and start_date != datetime.datetime.min):
            start_date = start_date - datetime.timedelta(minutes=offsetMins)

        if filename == 'live.xml':
            print "Fetching data from Dexcom via USB."
            Dexcom.LocateAndDownload(start_date)
            print "Fetch finished."
        else:
            print "In simulator mode. Sample data being read from " + filename

        tree = ET.parse(filename)
        root = tree.getroot()

        print "Pushing data to web service..."
        senddata(root.find('GlucoseReadings'), lastTime)
        print 'Done. Going to sleep for 1 minute. zzz'
        time.sleep(60)
