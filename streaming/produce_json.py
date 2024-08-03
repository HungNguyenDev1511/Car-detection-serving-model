import argparse
import io
import json
import os
from datetime import datetime
from time import sleep
import random

import numpy as np
from bson import json_util
from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic

parser = argparse.ArgumentParser()
parser.add_argument(
    "-m",
    "--mode",
    default="setup",
    choices=["setup", "teardown"],
    help="Whether to setup or teardown a Kafka topic with driver stats events. Setup will teardown before beginning emitting events.",
)
parser.add_argument(
    "-b",
    "--bootstrap_servers",
    default="localhost:9092",
    help="Where the bootstrap server is",
)
parser.add_argument(
    "-c",
    "--schemas_path",
    default="./avro_schemas",
    help="Folder containing all generated avro schemas",
)
parser.add_argument(
    "-i",
    "--image_dir",
    default="./images",
    help="Directory containing the images to send",
)

args = parser.parse_args()

image_id_counter = 1  

def create_topic(admin, topic_name):
    # Create topic if not exists
    try:
        # Create Kafka topic
        topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
        admin.create_topics([topic])
        print(f"A new topic {topic_name} has been created!")
    except Exception:
        print(f"Topic {topic_name} already exists. Skipping creation!")
        pass


def create_streams(servers, schemas_path, image_dir):
    producer = None
    admin = None
    for _ in range(10):
        try:
            producer = KafkaProducer(bootstrap_servers=servers)
            admin = KafkaAdminClient(bootstrap_servers=servers)
            print("SUCCESS: instantiated Kafka admin and producer")
            break
        except Exception as e:
            print(
                f"Trying to instantiate admin and producer with bootstrap servers {servers} with error {e}"
            )
            sleep(10)
            pass

    image_files = [
        os.path.join(image_dir, f)
        for f in os.listdir(image_dir)
        if os.path.isfile(os.path.join(image_dir, f))
    ]
    image_index = 0

    while True:
        image_file = image_files[image_index]
        image_index = (image_index + 1) % len(image_files)

        with open(image_file, "rb") as img_file:
            image_data = img_file.read()

        record = {
            "schema": {
                "type": "struct",
                "fields": [
                    {"type": "int64", "optional": False, "field": "image_id"},
                    {"type": "bytes", "optional": False, "field": "image_data"},
                ],
            }
        }
        record["payload"] = {}

        record["payload"]["image_id"] = image_id_counter 
        image_id_counter += 1 # tanc chi so image id
        record["payload"]["image_data"] = image_data


        # Get topic name for this image
        topic_name = f"image_0"

        # Create a new topic for this image if not exists
        create_topic(admin, topic_name=topic_name)

        # Send messages to this topic
        producer.send(
            topic_name, json.dumps(record, default=json_util.default).encode("utf-8")
        )
        print(record)
        sleep(2)


def teardown_stream(topic_name, servers=["localhost:9092"]):
    try:
        admin = KafkaAdminClient(bootstrap_servers=servers)
        print(admin.delete_topics([topic_name]))
        print(f"Topic {topic_name} deleted")
    except Exception as e:
        print(str(e))
        pass


if __name__ == "__main__":
    parsed_args = vars(args)
    mode = parsed_args["mode"]
    servers = parsed_args["bootstrap_servers"]
    image_dir = parsed_args["image_dir"]

    # Tear down all previous streams
    print("Tearing down all existing topics!")
    for image_id in range(NUM_IMAGE):
        try:
            teardown_stream(f"image_{image_id}", [servers])
        except Exception as e:
            print(f"Topic image_{image_id} does not exist. Skipping...!")

    if mode == "setup":
        schemas_path = parsed_args["schemas_path"]
        create_streams([servers], schemas_path, image_dir)
