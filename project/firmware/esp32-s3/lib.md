# Required Libraries

## Adafruit Libraries (download from CircuitPython Bundle)
- adafruit_scd30.mpy - Library for SCD30 CO2, Temperature, and Humidity Sensor
- adafruit_minimqtt/adafruit_minimqtt.mpy - Library for MQTT protocol
- adafruit_minimqtt/matcher.mpy - Dependency for adafruit_minimqtt
- adafruit_connection_manager.mpy - Dependency for adafruit_minimqtt
- adafruit_ticks.mpy - Dependency for adafruit_minimqtt

## Hardware Connections
1. **SCD30 Sensor**: Connect to I2C Grove port on Grove Shield
2. **Light Sensor v1.1**: Connect to A0 Grove port on Grove Shield. Can also use A2 or A4 (update `board.A0` in code)
