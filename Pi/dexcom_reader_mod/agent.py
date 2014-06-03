
import xml.etree.ElementTree as ET
import time
import requests
import datetime
import calendar
import sys
from readdata import Dexcom
from filesender import senddata


if __name__ == '__main__':
    while 1:
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

        # if a parameter is included, it represents the MINUTES to subtract from the start date
        # A value of 10 means that data will be grabbed since 10 minutes before lastTime
        if (len(sys.argv) == 2 and start_date != datetime.datetime.min):
            start_date = start_date - datetime.timedelta(minutes=int(sys.argv[1]))

        print "Fetching data from Dexcom via USB."
        Dexcom.LocateAndDownload(start_date)
        print "Fetch finished."

        filename = 'output.xml'
        tree = ET.parse(filename)
        root = tree.getroot()

        print "Pushing data to web service..."
        senddata(root.find('GlucoseReadings'), lastTime)
        print 'Done. Going to sleep for 1 minute. zzz'
        time.sleep(60)
