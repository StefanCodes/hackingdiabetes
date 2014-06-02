
import xml.etree.ElementTree as ET
import time
import requests
from datetime import datetime
import calendar
import sys
from readdata import Dexcom
from filesender import senddata


if __name__ == '__main__':
    if (len(sys.argv) == 1):
        start_date = datetime.min
    else:
        start_date = datetime.now() - timedelta(minutes=int(sys.argv[1]))
    
    Dexcom.LocateAndDownload(start_date)
    filename = 'output.xml'
    tree = ET.parse(filename)
    root = tree.getroot()
    lastTime = 0
    
    #try:
    f = open('last-time.txt', 'r+')
    lastTime = int(f.readline())
    f.close()
	#except:
	#	pass #do nothing
    senddata(root.find('GlucoseReadings'), lastTime)
