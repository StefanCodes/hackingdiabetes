import xml.etree.ElementTree as ET
import time
import requests

tree = ET.parse('Dexcom.xml')

root = tree.getroot()

for reading in root.find('GlucoseReadings'):
	print 'got another reading'
	print reading.get('DisplayTime'), reading.get('Value')
	time.sleep(1)
	payload = {'value': float(reading.get('Value'))}
	requests.post("http://wotkit.sensetecnic.com/api/sensors/mike.blood-sensor/data", auth=('b781be7908b3787b', 'f5bde2beb22a0653'), data=payload)

