
'''
Sends reading data to Wotkit in format {'msg':(fast_deviating, time_to_go), 'timestamp':int, 'value':int}
See Glucose_Predictor for 'msg' value details.

Also sends a text and iOS alert if glucose levels are rising or falling too fast

'''

import xml.etree.ElementTree as ET
import time
import requests
from datetime import datetime
import calendar
import sys
import pytz, datetime
from Glucose_Predictor import Glucose_Predictor
from send_alerts import send_alerts


def senddata(readings, lastTime):
	'''assumes this is a list of readings with a DisplayTime and Value
	attribute.  Assume DisplayTime is current time zone'''

	for reading in readings:
		timestamp_str = reading.get('DisplayTime')

		local_tz = pytz.timezone ("US/Pacific")
		naive_dt = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
		local_dt = local_tz.localize(naive_dt)
		utc_dt = local_dt.astimezone (pytz.utc)

		timestamp=calendar.timegm(utc_dt.utctimetuple())
		value = float(reading.get('Value'))
		# send the data to the wotkit if its new, and send alerts if needed
		if timestamp > lastTime:
			prediction = Glucose_Predictor(value)

			payload = {'msg':(prediction[0], prediction[2]), 'timestamp':timestamp*1000, 'value': float(reading.get('Value'))}
			print payload

			if (prediction[0] == 1):
				send_alerts('#rising')
				print 'sent rising alert'
			elif (prediction[0] == -1):
				send_alerts('#falling')
				print 'sent falling alert'

			#send info to wotkit
			print "sending data"
			r = requests.post("http://wotkit.sensetecnic.com/api/sensors/hackathon.glucose/data", auth=('hackathon', 'HHVan2014'), data=payload)
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

	senddata(root.find('GlucoseReadings'), lastTime)