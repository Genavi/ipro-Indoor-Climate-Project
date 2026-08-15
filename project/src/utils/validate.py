import os
import sys
import logging
import socket

logger = logging.getLogger(__name__)

def validate_env_vars():
    """Validate that all required environment variables are set."""
    required_vars = {
        'SERIAL_PORT': 'Serial port path (e.g., /dev/ttyUSB0)',
        'BAUDRATE': 'Baud rate for serial communication',
        'MQTT_BROKER': 'MQTT broker hostname or IP address',
        'MQTT_PORT': 'MQTT broker port number',
        'MQTT_USERNAME': 'MQTT username',
        'MQTT_PASSWORD': 'MQTT password',
        'OUTPUT_METHOD': 'Output method (database or mqtt)'
    }

    if os.getenv('OUTPUT_METHOD') == 'database':
        required_vars.update({
            'DATABASE_HOST': 'Database hostname or IP address',
            'DATABASE_PORT': 'Database port number',
            'DATABASE_USER': 'Database username',
            'DATABASE_PASSWORD': 'Database password',
            'DATABASE_NAME': 'Database name'
        })

    missing_vars = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value is None or value.strip() == '':
            missing_vars.append(f"  - {var}: {description}")
            logger.error(f"Missing or empty environment variable: {var}")
        else:
            display_value = '***' if 'PASSWORD' in var else value
            logger.info(f"Loaded {var}={display_value}")

    if missing_vars:
        error_msg = "Missing required environment variables:\n" + "\n".join(missing_vars)
        logger.error(error_msg)
        logger.error("Please ensure all environment variables are set in your .env file or systemd service configuration")
        sys.exit(1)

def check_network_connectivity(hostname):
    """Check if hostname can be resolved (basic connectivity check)."""
    try:
        socket.gethostbyname(hostname)
        return True
    except socket.gaierror:
        return False
