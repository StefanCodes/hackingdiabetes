
UPLOAD_TO_WOTKIT = True
WOTKIT_UPLOAD_INTERVAL = 60

WOTKIT_API_BASE = 'http://wotkit.sensetecnic.com/'
WOTKIT_USERNAME = 'username'
WOTKIT_PASSWORD = 'password'
WOTKIT_SENSOR_NAME = "blood-glucose"

# information used to register sensor.
# TODO: add schema fields - see http://wotkit.readthedocs.org/en/latest/api_v1/api_sensors.html
WOTKIT_SENSOR = {
    "visibility":"PRIVATE",
    "name":WOTKIT_SENSOR_NAME,
    "description":"Dexcom blood glucose readings",
    "longName":"Blood Glucose"
}
