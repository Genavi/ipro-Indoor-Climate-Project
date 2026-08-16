import adafruit_scd30
import board
import time
import json

sensor = adafruit_scd30.SCD30(board.I2C())

READER_ID = 1
LOCATION_ID = 1
TOPIC = "sensors/feathers3"

while True:
    try:
        co2 = sensor.CO2
        temperature = sensor.temperature
        fahrenheit = temperature * 9 / 5 + 32
        humidity = sensor.relative_humidity

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
            print(f"{json.dumps(payload)}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(5)
