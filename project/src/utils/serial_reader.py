import serial

from datetime import datetime, timezone

from src.database.connection import SessionLocal
from src.database.models import SensorReading

def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def start_reading(port, baudrate):
    print(f"Reading data from serial port {port} using baudrate {baudrate}...")

    try:
        port = serial.Serial(port)
        port.baudrate = int(baudrate)

        while (port.isOpen()):
            bytes = port.readline()
            chars = str(bytes, 'utf-8')

            try:
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
            except ValueError as e:
                print(f"Could not parse data: {e}\nError occured during processing of line: {chars}")
    except KeyboardInterrupt:
        print("Stopping serial reading...")


def save_to_database(sensor_0_name, sensor_0_value, sensor_1_name=None, sensor_1_value=None,
                     sensor_2_name=None, sensor_2_value=None, sensor_3_name=None,
                     sensor_3_value=None, sensor_4_name=None, sensor_4_value=None):
    db = SessionLocal()
    try:
        reading = SensorReading(
            timestamp=datetime.now(timezone.utc),
            reader=1,
            location=1,
            sensor_0_name=sensor_0_name,
            sensor_0_value=sensor_0_value,
            sensor_1_name=sensor_1_name,
            sensor_1_value=sensor_1_value,
            sensor_2_name=sensor_2_name,
            sensor_2_value=sensor_2_value,
            sensor_3_name=sensor_3_name,
            sensor_3_value=sensor_3_value,
            sensor_4_name=sensor_4_name,
            sensor_4_value=sensor_4_value
        )
        db.add(reading)
        db.commit()
        print(f"[{reading.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] Inserted: co2={sensor_0_value}, humidity={sensor_1_value if sensor_1_value is not None else 'N/A'}, temperature={sensor_2_value if sensor_2_value is not None else 'N/A'}, celcius={sensor_3_value if sensor_3_value is not None else 'N/A'}, fahrenheit={sensor_4_value if sensor_4_value is not None else 'N/A'}")
    except Exception as e:
        db.rollback()
        print(f"Error inserting data into the database: {e}")
    finally:
        db.close()
