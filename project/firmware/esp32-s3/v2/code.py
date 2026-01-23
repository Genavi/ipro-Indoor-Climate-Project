print("Hello World!")
import adafruit_scd30
import wifi
import board
import time

sensor = adafruit_scd30.SCD30(board.I2C())

while True:
    try:
        co2 = sensor.CO2
        temperature = sensor.temperature
        fahrenheit = temperature * 9 / 5 + 32
        celcius = temperature
        humidity = sensor.relative_humidity
        print(f"CO2: {co2} ppm, Temperature: {temperature} °C, {fahrenheit} °F, Humidity: {humidity} %")
    except Exception as e:
        print(f"Error reading sensor data: {e}")
    time.sleep(5)
