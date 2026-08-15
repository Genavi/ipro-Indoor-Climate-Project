import serial
import json
import logging

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
                        save_to_database(
                            sensor_0_name='CO2',
                            sensor_0_value=to_float(data[0]),
                            sensor_1_name='Humidity',
                            sensor_1_value=to_float(data[1]) if len(data) > 1 else None,
                            sensor_2_name='Temperature',
                            sensor_2_value=to_float(data[2]) if len(data) > 2 else None,
                            sensor_3_name='Celcius Temperature',
                            sensor_3_value=to_float(data[3]) if len(data) > 3 else None,
                            sensor_4_name='Fahrenheit Temperature',
                            sensor_4_value=to_float(data[4]) if len(data) > 4 else None
                        )
                    
                    case "mqtt":
                        write_mqtt(client, json.loads(chars))
                    case _:
                        logger.warning(f"Unknown output method: {output}")
            except ValueError as e:
                logger.error(f"Could not parse data: {e}\nError occured during processing of line: {chars}")
    except KeyboardInterrupt:
        logger.info("Stopping serial reading...")
