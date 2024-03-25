# pylint: disable=all
from paho.mqtt import client as mqtt_client
import json
import time
from schema.aggregated_data_schema import AggregatedDataSchema
from file_datasource import FileDatasource
import config


def connect_mqtt(broker, port):
    """Create MQTT client"""
    print(f"CONNECT TO {broker}:{port}")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
        else:
            print("Failed to connect {broker}:{port}, return code %d\n", rc)
            exit(rc)  # Stop execution

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client


def publish(client, topic, datasource, delay):
    datasource.startReading()
    while True:
        time.sleep(delay)
        accelerometer_data = datasource.read_csv_file(datasource.accelerometer_filename)
        gps_data = datasource.read_csv_file(datasource.gps_filename)
        parking_data = datasource.read_csv_file(datasource.parking_filename)

        for accel_data, gps_data, parking_data in zip(accelerometer_data, gps_data, parking_data):
            data = {
                "accelometer": {
                    "x": accel_data[0],
                    "y": accel_data[1],
                    "z": accel_data[2]
                },
                "gps": {
                    "longitude": gps_data[0],
                    "latitude": gps_data[1]
                },
                "parking": {
                    "empty_count": parking_data[0],
                    "gps": { 
                        "longitude": parking_data[1],
                        "latitude": parking_data[2]
                    }
                }
            }

            msg = json.dumps(data)
            result = client.publish(topic, msg)
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")


def run():
    # Prepare mqtt client
    client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)
    # Prepare datasource
    datasource = FileDatasource("data/accelerometer.csv", "data/gps.csv", "data/parking.csv")
    # Infinity publish data

    publish(client, config.MQTT_TOPIC, datasource, config.DELAY)


if __name__ == "__main__":
    run()
