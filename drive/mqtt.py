from paho.mqtt import client as mqtt_client
from config.mqtt import client_id, username, password, broker, port

def connectMqtt():
    client = mqtt_client.Client(client_id + "drive")
    client.username_pw_set(username, password)
    client.on_connect = print("MQTT client connected as sender for drive")
    client.connect(broker, port)
    return client
