import serial
import json
import logging

from src.utils.database import save_multiple_readings
from src.utils.mqtt import write_mqtt

logger = logging.getLogger(__name__)

def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def start_reading(port, baudrate, output="database", client=None):
    logger.info(f"Reading data from serial port {port} using baudrate {baudrate}...")

    try:
        port = serial.Serial(port)
        port.baudrate = int(baudrate)

        while (port.isOpen()):
            bytes = port.readline()
            chars = str(bytes, 'utf-8')

            try:
                match output:
                    case "database":
                        data = chars.split(';')
                        readings = []

                        if len(data) > 0 and data[0]:
                            readings.append({
                                'sensor_type': 'co2',
                                'value': to_float(data[0]),
                                'unit': 'ppm'
                            })
                        if len(data) > 1 and data[1]:
                            readings.append({
                                'sensor_type': 'humidity',
                                'value': to_float(data[1]),
                                'unit': '%'
                            })
                        if len(data) > 2 and data[2]:
                            readings.append({
                                'sensor_type': 'temperature',
                                'value': to_float(data[2]),
                                'unit': '°C'
                            })

                        valid_readings = [r for r in readings if r['value'] is not None]
                        if valid_readings:
                            save_multiple_readings(valid_readings)

                    case "mqtt":
                        write_mqtt(client, json.loads(chars))
                    case _:
                        logger.warning(f"Unknown output method: {output}")
            except ValueError as e:
                logger.error(f"Could not parse data: {e}\nError occured during processing of line: {chars}")
    except KeyboardInterrupt:
        logger.info("Stopping serial reading...")
