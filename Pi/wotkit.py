import requests
import json
from settings import *

class WoTKitClient(object):
    """ minimal wotkit client """

    def __init__(self, name=WOTKIT_USERNAME, password=WOTKIT_PASSWORD):
        self.name = name
        self.password = password

    def set_credentials(name, password):
        """ set credentials to something other than the default """
        self.name = name
        self.password = password

    def send_data(self, sensorname, payload):
        """ send a data dict to the wotkit
            must contain a timestamp (unix millis) and follow the sensor schema
        """
        r = requests.post(WOTKIT_API_BASE+'api/sensors/{0}/data'.format(sensorname), auth=(self.name, self.password), data=payload)
        return r

    def register_sensor(self):
        """ register a sensor with the wotkit """
        headers = {'content-type': 'application/json'}
        payload = WOTKIT_SENSOR

        r = requests.post(WOTKIT_API_BASE+'api/sensors', auth=(self.name, self.password),
            headers=headers, data=json.dumps(payload))
        return r

