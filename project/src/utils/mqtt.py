import logging
import json

logger = logging.getLogger(__name__)

def write_mqtt(client, data):

    if client is None:
        logger.error("MQTT client is not connected. Cannot publish data.")
        return

    topic = f"sensors/feathers3/{data['sensor_type']}"
    client.publish(topic, json.dumps(data))
    print(f"Published: {data}")
