import random
import signal
import json
import sys
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

TOPIC = 'test'
CLIENTID = 'KIBANDI'
BROKER_HOST = "localhost"
BROKER_PORT = 1883
client = None

# function to subscribe when the connection is established


def onconnect(client, user_data, flags, connection_result_code):
    if connection_result_code == 0:
        print('Connection successful')
    else:
        print('Connection not successful')

    client.subscribe(TOPIC, qos=2)
    pubishdata(client)

# function to handle disconnection


def ondisconnect(client, user_data, disconnection_result_code):
    print('Disconnected')

# function to publish data


def pubishdata(client):
    for i in range(1000):
        value = random.randint(0, 100)
        payload = {
            "value": value,
            "data": "sensor",
            "description": "sitting room temperature"
        }
        finalvalue = json.dumps(payload)
        print('>>>>{}'.format(str(finalvalue)))
        publish.single(TOPIC, finalvalue)
        print('published')
        time.sleep(1.0)


def signal_handler(sig, frame):
    """Capture Control+C and disconnect from Broker."""

    print("You pressed Control + C. Shutting down, please wait...")

    client.disconnect()  # Graceful disconnection.
    sys.exit(0)


def initmqtt():
    global client

    client = mqtt.Client(client_id=CLIENTID, clean_session=False)

    client.on_connect = onconnect
    client.on_disconnect = ondisconnect

    client.connect(BROKER_HOST, BROKER_PORT)


# initialize module
initmqtt()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Capture Control + C
    client.loop_forever()
