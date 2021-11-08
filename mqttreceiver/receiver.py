import signal
import sys
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

TOPIC = 'test'
CLIENTID = 'KIBANDI'
BROKER_HOST = "localhost"
BROKER_PORT = 1883
client = None


def onconnect(client, user_data, flags, connection_result_code):
    if connection_result_code == 0:
        print('Connection successful')
    else:
        print('Connection not successful')

    client.subscribe(TOPIC, qos=2)

# function to handle disconnection


def ondisconnect(client, user_data, disconnection_result_code):
    print('Disconnected')


def onmessage(client, userdata, msg):
    msg_val = json.loads(msg.payload)  # convert string to JSON
    print('temp from:{}  >>{} degrees Celsius'.format(
        msg_val['description'], msg_val['value']))


def initmqtt():
    global client

    client = mqtt.Client(client_id=CLIENTID, clean_session=False)

    client.on_connect = onconnect
    client.on_disconnect = ondisconnect
    client.on_message = onmessage

    client.connect(BROKER_HOST, BROKER_PORT)


def signal_handler(sig, frame):
    print("You pressed Control + C. Shutting down, please wait...")

    client.disconnect()  # Graceful disconnection.
    sys.exit(0)


# initialize module
initmqtt()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Capture Control + C
    client.loop_forever()
