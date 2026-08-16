import adafruit_scd30
import board
import time
import json
import analogio

sensor = adafruit_scd30.SCD30(board.I2C())
light_sensor = analogio.AnalogIn(board.A0)

READER_ID = 1
LOCATION_ID = 1
TOPIC = "sensors/feathers3"

def read_scd30_sensor():
    """
    Read data from the SCD30 sensor.

    Returns:
        dict: A dictionary containing CO2, temperature, and humidity readings.
    """
    return {
        "co2": sensor.CO2,
        "temperature": sensor.temperature,
        "humidity": sensor.relative_humidity
    }

def read_light_percentage():
    """
    Read light sensor and convert to percentage (0-100%).
    Grove Light Sensor outputs voltage proportional to light intensity.
    """
    raw_value = light_sensor.value
    voltage = (raw_value / 65535) * 3.3
    percentage = (voltage / 3.3) * 100
    
    return percentage

while True:
    try:      
        readings = read_scd30_sensor()
        light = read_light_percentage()

        payloads = [
            ("co2", "ppm", readings["co2"]),
            ("temperature", "°C", readings["temperature"]),
            ("temperature", "°F", readings["temperature"] * 9 / 5 + 32),
            ("humidity", "%", readings["humidity"]),
            ("light", "%", light)
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
