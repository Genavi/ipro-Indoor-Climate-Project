import os
import serial
import psycopg2

from dotenv import load_dotenv


load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    print("Connected to the database successfully.")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit()


port = serial.Serial(os.getenv("PORT"))
port.baudrate = int(os.getenv("BAUDRATE"))

while (port.isOpen()):
    print(f"Reading data from serial port {os.getenv('PORT')}...")
    bytes = port.readline()
    chars = str(bytes, 'utf-8')

    try:
        data = chars.split(';')
        cur = conn.cursor()
        sql = "INSERT INTO sensor_readings (timestamp, reader, location, sensor_0_name, sensor_0_value, sensor_1_name, sensor_1_value, sensor_2_name, sensor_2_value, sensor_3_name, sensor_3_value, sensor_4_name, sensor_4_value) VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cur.execute(sql, (1, 1, 'CO2', data[0], 'Humidity', data[1] if len(data) > 1 else None, 'Temperature', data[2] if len(data) > 2 else None, 'Celcius Temperature', data[3] if len(data) > 3 else None, 'Fahrenheit Temperature', data[4] if len(data) > 4 else None))
        print(f'Inserted: CO2={data[0]}, Humidity={data[1] if len(data) > 1 else "N/A"}, Temperature={data[2] if len(data) > 2 else "N/A"}, Cel_Temp={data[3] if len(data) > 3 else "N/A"}, Far_Temp={data[4] if len(data) > 4 else "N/A"}')
    except Exception as e:
        print(f"Error inserting data into the database: {e}\nError occured during processing of line: {chars}")
    finally:
        cur.close()
        conn.commit()
