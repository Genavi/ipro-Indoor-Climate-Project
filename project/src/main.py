import os
import logging

from dotenv import load_dotenv
from paho.mqtt.enums import CallbackAPIVersion

from src.utils.serial_reader import start_reading
from src.utils.database import run_migrations
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

ser = serial.Serial(os.getenv('SERIAL_PORT'), int(os.getenv('BAUDRATE')))

client = mqtt.Client(CallbackAPIVersion.VERSION2)
client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))
client.connect(os.getenv('MQTT_BROKER'), int(os.getenv('MQTT_PORT')), 60)

def main():
    if os.getenv("OUTPUT_METHOD") == "database":
        run_migrations()
    start_reading(os.getenv("SERIAL_PORT"), os.getenv("BAUDRATE"), os.getenv("OUTPUT_METHOD"), client)

if __name__ == "__main__":
    main()
