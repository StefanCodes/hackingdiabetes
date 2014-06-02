import xml.etree.ElementTree as ET
import time
import requests
from datetime import datetime
import calendar
import sys

def senddata(readings, lastTime):
	'''assumes this is a list of readings with a DisplayTime and Value
	attribute.  Assume DisplayTime is current time zone'''

	for reading in readings:
		timestamp_str = reading.get('DisplayTime')
		dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
		timestamp=calendar.timegm(dt.utctimetuple())
		value = float(reading.get('Value'))
		payload = {'timestamp':timestamp*1000, 'value': float(reading.get('Value'))}
		print payload
		# send the data to the wotkit if its new
		if timestamp > lastTime:
			print "sending data"
			r = requests.post("http://wotkit.sensetecnic.com/api/sensors/mike.glucose/data", auth=('b781be7908b3787b', 'f5bde2beb22a0653'), data=payload)
			print r.status_code
			f = open('last-time.txt', 'w+')
			f.write(str(timestamp)+'\n')
			f.close()	
		else:
			print "skipping - old data"

if __name__ == "__main__":
	filename = sys.argv[1]
	tree = ET.parse(filename)
	root = tree.getroot()

	lastTime = 0
	try:
		f = open('last-time.txt', 'r+')
		lastTime = int(f.readline())
		f.close()
	except:
		pass #do nothing

	sendData(root.find('GlucoseReadings'), lastTime)




