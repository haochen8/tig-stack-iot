import sys
sys.path.append('lib')

import lib.dht as dht
import machine
import time
import lib.wifiConnection as wifiConnection
from umqtt.simple import MQTTClient
import json

# MQTT Broker Settings
MQTT_BROKER = "192.168.10.157"
MQTT_PORT = 1883
MQTT_TOPIC = "test/dht11"

# DHT11 Sensor
tempSensor = dht.DHT11(machine.Pin(27)) # DHT11 Constructor 

# WiFi Connection
ip = wifiConnection.connect()
print("Device IP:", ip)

# MQTT Connection
client = MQTTClient("pico_client", MQTT_BROKER, port=MQTT_PORT)
client.connect()

while True:
    try:
        tempSensor.measure()
        temperature = tempSensor.temperature()
        humidity = tempSensor.humidity()
        print("Temperature: {} °C | Humidity: {} %".format(temperature, humidity))

        payload = json.dumps({
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": time.time()
        })

        client.publish(MQTT_TOPIC, payload)
        print("Published to MQTT")
    except Exception as error:
        print("Error:", error)
    time.sleep(300)  # Every 5 minutes
