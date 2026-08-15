print("Hello World!")
import adafruit_scd30
import wifi
import board
import time
import socketpool
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import json

sensor = adafruit_scd30.SCD30(board.I2C())

WIFI_SSID = "WIFI_SSID"
WIFI_PASSWORD = "WIFI_PASSWORD"
MQTT_BROKER = "BROKER_IP_OR_HOSTNAME"
MQTT_PORT = 1883
MQTT_USERNAME = "admin"
MQTT_PASSWORD = "MQTT_PASSWORD"
READER_ID = 1
LOCATION_ID = 1
TOPIC = "sensors/feathers3"

print(f"Connecting to {WIFI_SSID}...")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
print(f"✓ Connected! IP: {wifi.radio.ipv4_address}")

pool = socketpool.SocketPool(wifi.radio)

mqtt_client = MQTT.MQTT(
    broker=MQTT_BROKER,
    port=MQTT_PORT,
    username=MQTT_USERNAME,
    password=MQTT_PASSWORD,
    socket_pool=pool,
    ssl_context=None,
    keep_alive=60,
)

print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}...")
mqtt_client.connect()
print("✓ Connected to MQTT broker!")


# Main loop
while True:
    try:
        mqtt_client.loop()
        
        co2 = sensor.CO2
        temperature = sensor.temperature
        fahrenheit = temperature * 9 / 5 + 32
        humidity = sensor.relative_humidity
        
        print(f"CO2: {co2:.2f} ppm, Temp: {temperature:.2f}°C, Humidity: {humidity:.2f}%")

        payloads = [
            ("co2", "ppm", co2),
            ("temperature", "°C", temperature),
            ("temperature", "°F", fahrenheit),
            ("humidity", "%", humidity)
        ]
        
        for sensor_type, unit, value in payloads:
            payload = {
                "reader": READER_ID,
                "location": LOCATION_ID,
                "topic": f"{TOPIC}/{sensor_type}",
                "unit": unit,
                "sensor_type": sensor_type,
                "value": value
            }
            mqtt_client.publish(f"{TOPIC}/{sensor_type}", json.dumps(payload))
        
        print("✓ Data published")
        
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(10)