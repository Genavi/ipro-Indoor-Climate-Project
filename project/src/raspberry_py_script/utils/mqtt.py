import os
import time
import logging
import json
import socket
import paho.mqtt.client as mqtt

from paho.mqtt.enums import CallbackAPIVersion
from utils.validate import check_network_connectivity

logger = logging.getLogger(__name__)

def connect_mqtt_with_retry(max_retries=5, retry_delay=5):
    """
    Connect to MQTT broker with retry logic.

    Args:
        max_retries: Maximum number of connection attempts.
        retry_delay: Delay between retries in seconds.

    Returns:
        MQTT client instance if connection is successful.

    Raises:
        Exception if connection fails after maximum retries.
    """

    mqtt_broker = os.getenv('MQTT_BROKER')
    mqtt_port = int(os.getenv('MQTT_PORT'))
    mqtt_username = os.getenv('MQTT_USERNAME')
    mqtt_password = os.getenv('MQTT_PASSWORD')

    client = mqtt.Client(CallbackAPIVersion.VERSION2)
    client.username_pw_set(mqtt_username, mqtt_password)

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Attempting to connect to MQTT broker at {mqtt_broker}:{mqtt_port} (attempt {attempt}/{max_retries})")

            if not check_network_connectivity(mqtt_broker):
                logger.warning(f"Cannot resolve hostname '{mqtt_broker}'. Possible causes:")
                logger.warning("  - Device not connected to VPN (Tailscale, WireGuard, etc.)")
                logger.warning("  - DNS server not configured correctly")
                logger.warning("  - Hostname/IP address is incorrect")
                logger.warning("  - Network connectivity issues")
                if 'tail' in mqtt_broker.lower() or '.ts.' in mqtt_broker:
                    logger.warning("  → This looks like a Tailscale hostname - ensure Tailscale is running:")
                    logger.warning("     sudo systemctl status tailscaled")
                    logger.warning("     tailscale status")

            client.connect(mqtt_broker, mqtt_port, 60)
            logger.info(f"Successfully connected to MQTT broker at {mqtt_broker}:{mqtt_port}")
            return client
        except socket.gaierror as e:
            logger.error(f"DNS resolution failed for '{mqtt_broker}': {e}")
            logger.error("This typically means:")
            logger.error("  - The hostname cannot be found in DNS")
            logger.error("  - You're not connected to the required VPN/network")
            logger.error("  - The MQTT_BROKER environment variable is incorrect")
            if attempt < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Failed to resolve MQTT broker hostname after {max_retries} attempts")
                logger.error("Please check network connectivity and VPN status before restarting the service")
                raise
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker (attempt {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Failed to connect to MQTT broker after {max_retries} attempts")
                raise

def write_mqtt(client, data):
    """
    Publish sensor data to MQTT broker.

    Args:
        client: MQTT client instance.
        data: Dictionary containing sensor data with keys 'sensor_type', 'value', and 'unit'.
    """

    if client is None:
        logger.error("MQTT client is not connected. Cannot publish data.")
        return

    topic = f"sensors/feathers3/{data['sensor_type']}"
    client.publish(topic, json.dumps(data))
    print(f"Published: {data}")
