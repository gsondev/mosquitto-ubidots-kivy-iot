import json
import paho.mqtt.publish as publish

OUTBOUND_TOPIC = "/v1.6/devices/iot-test/"
BROKER_URL = "industrial.api.ubidots.com"
BROKER_PORT = 1883
UBIDOTS_TOKEN = "BBUS-BMpSID9WV8ssLcqOEG9nZnboFLDkep"
class UbidotsPublisher:
    @staticmethod
    def send_message(variable, message):
        try:
            credentials = {'username': UBIDOTS_TOKEN, 'password': ''}
            value = json.dumps({'value': message})
            print(OUTBOUND_TOPIC + variable, value, BROKER_URL)
            publish.single(OUTBOUND_TOPIC + variable, value,
                           hostname=BROKER_URL,
                           port=BROKER_PORT, auth=credentials)
        except Exception as ex:
            print("Error enviando mensaje ex: {}".format(ex))