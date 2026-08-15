import os
import sys
import logging

from dotenv import load_dotenv

from src.utils.serial_reader import start_reading
from src.utils.database import run_migrations
from src.utils.validate import validate_env_vars
from src.utils.mqtt import connect_mqtt_with_retry

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

def main():
    try:
        logger.info("Starting IoT MQTT Bridge")
        validate_env_vars()

        client = connect_mqtt_with_retry()

        serial_port = os.getenv('SERIAL_PORT')
        baudrate = os.getenv('BAUDRATE')
        logger.info(f"Initializing serial connection on {serial_port} at {baudrate} baud")

        if os.getenv("OUTPUT_METHOD") == "database":
            logger.info("Running database migrations")
            run_migrations()

        logger.info(f"Starting serial reader with output method: {os.getenv('OUTPUT_METHOD')}")
        start_reading(serial_port, baudrate, os.getenv("OUTPUT_METHOD"), client)

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down gracefully")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
