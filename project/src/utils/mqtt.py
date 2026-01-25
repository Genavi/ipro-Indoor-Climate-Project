import json

def write_mqtt(client, data): 
    topic = f"sensors/feathers3/{data['sensor_type']}"
    client.publish(topic, json.dumps(data))
    print(f"Published: {data}")
