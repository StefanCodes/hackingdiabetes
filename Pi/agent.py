import xml.etree.ElementTree as ET
import time
import requests # http://docs.python-requests.org/en/latest/
import datetime
import calendar
import sys
import random
from settings import *
from readdata import Dexcom
from filesender import senddata

# generate galues between 0.30 and 0.70 
SIM_MIN_VALUE = 30
SIM_MAX_VALUE = 70
SIM_DIVISOR = 10

# We intended to use JSON as our interchange format, but there's a lot of prior art using XML
# so let's burn that bridge later.
def SimulateXmlRecord():
	root = ET.Element("Patient")
	root.set("SerialNumber", "AA12345678")
	glucoseReadings = ET.SubElement(root,"GlucoseReadings")
	glucose = ET.SubElement(glucoseReadings,"Glucose")
	glucose.set("InternalTime", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	glucose.set("DisplayTime", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	glucose.set("Value", str(random.randint(SIM_MIN_VALUE,SIM_MAX_VALUE)/SIM_DIVISOR))
	tree = ET.ElementTree(root)
	return tree;

#Usage: py agent.py sourceFile [-sim]
if __name__ == '__main__':
	inSimulation = 0
	if (len(sys.argv) > 1 and sys.argv[1] == '-sim'):
		inSimulation = 1

	while 1:
		lastTime = 0
		try:
			f = open('last-time.txt', 'r+')
			lastTime = int(f.readline())
			f.close()
		except:
			pass

		if (lastTime > 0):
			start_date = datetime.datetime.fromtimestamp(lastTime)
		else:
			start_date = datetime.datetime.min;

		if (inSimulation):
			print "In simulator mode. Generating sample record."
			xmlTree = SimulateXmlRecord()
		else:
			print "Fetching data from Dexcom via USB."
			xmlTree = Dexcom.LocateAndDownload(start_date)
		print "Fetch finished."

		root = xmlTree.getroot()

		print "Pushing data to web service..."
		senddata(root.find('GlucoseReadings'), lastTime)
		print 'Done. Going to sleep for {0} secs. zzz'.format(WOTKIT_UPLOAD_INTERVAL)
		time.sleep(WOTKIT_UPLOAD_INTERVAL)
