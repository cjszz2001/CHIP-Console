import sys, select, os
import AWSIoTPythonSDK
# sys.path.insert(0, os.path.dirname(AWSIoTPythonSDK.__file__))
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import zwaveconsole


host = "a1eamysgk8i65j-ats.iot.us-west-2.amazonaws.com"
rootCAPath = "./root-CA.crt"
certificatePath = "./console-cert.pem.crt"
privateKeyPath = "./console-private.pem.key"
port = 8883
clientId = "Zwave-Python-Console"

topic = "zwavegateway/zwave-gateway/request"
topic1 = "zwavegateway/zwave-gateway/report"

node = 0

my_aws_iot_mqtt_client = None
my_aws_iot_mqtt_client = AWSIoTMQTTClient(clientId)


# Custom MQTT message callback
def custom_callback(client, userdata, message):
    print("--------------------------------------")
    print("Received a new message: ")
    mqttmsg = message.payload.decode('UTF-8')
    print(mqttmsg)
    msg_dict = json.loads(mqttmsg)
    global node
    node = msg_dict['node_id']
    print("from topic: ")
    print(message.topic)
    print("--------------------------------------")


def configure_aws_connection():
    my_aws_iot_mqtt_client.configureEndpoint(host, port)
    my_aws_iot_mqtt_client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTClient connection configuration
    my_aws_iot_mqtt_client.configureAutoReconnectBackoffTime(1, 128, 20)
    my_aws_iot_mqtt_client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    my_aws_iot_mqtt_client.configureDrainingFrequency(2)  # Draining: 2 Hz
    my_aws_iot_mqtt_client.configureConnectDisconnectTimeout(10)  # 10 sec
    my_aws_iot_mqtt_client.configureMQTTOperationTimeout(100)  # 5 sec

    # Connect and subscribe to AWS IoT
    my_aws_iot_mqtt_client.connect()
    my_aws_iot_mqtt_client.subscribe(topic1, 0, custom_callback)
    time.sleep(2)


def toggleDimmer():
    flag = 1

    while True:
        message = {'device': "Switch", 'nodeid': node}
        flag ^= 1
        if flag:
            message['value'] = 1
        else:
            message['value'] = 0

        message_json = json.dumps(message)
        my_aws_iot_mqtt_client.publish(topic, message_json, 0)
        print('Published topic %s: %s\n' % (topic, message_json))
        time.sleep(6)

def turn_on_dimmer():
    message = {'device': "switch", 'value': 1, 'nodeid': node}
    message_json = json.dumps(message)
    my_aws_iot_mqtt_client.publish(topic, message_json, 0)
    print('Published topic %s: %s\n' % (topic, message_json))


def turn_off_dimmer():
    message = {'device': "switch", 'value': 0, 'nodeid': node}
    message_json = json.dumps(message)
    my_aws_iot_mqtt_client.publish(topic, message_json, 0)
    print('Published topic %s: %s\n' % (topic, message_json))


def add_device():
    message = {'device': "switch", 'nodeid': node, 'value': 2}
    message_json = json.dumps(message)
    my_aws_iot_mqtt_client.publish(topic, message_json, 0)
    print('Published topic %s: %s\n' % (topic, message_json))


def remove_device():
    message = {'device': "switch", 'nodeid': node, 'value': 3}
    message_json = json.dumps(message)
    my_aws_iot_mqtt_client.publish(topic, message_json, 0)
    print('Published topic %s: %s\n' % (topic, message_json))

