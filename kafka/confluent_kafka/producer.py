import os
import cv2
import sys
import confluent_kafka

from uuid import uuid4
from threading import Thread
from flask_restful import Resource ,Api
from flask import Flask , request , jsonify
from dataclasses import asdict, dataclass, field
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer

def image_to_dict(data,ctx):
    return dict(
        height = data.height,
        width = data.width,
        image = data.image
    )



class Image_Type(object):
    def __init__(self,height,width,image):
        self.height = height 
        self.width = width
        self.image = image




def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.
    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    Note:
        In the delivery report callback the Message.key() and Message.value()
        will be the binary format as encoded by any configured Serializers and
        not the same object that was passed to produce().
        If you wish to pass the original object(s) for key and value to delivery
        report callback we recommend a bound callback or lambda where you pass
        the objects along.
    """
    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))

schema_str = """
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "transfer json data",
    "description": "A Confluent Kafka Python User",
    "type": "object",
    "properties": {
    "height": {
        "description": "height of image",
        "type": "int",
        "exclusiveMinimum": 1
    },
    "width": {
        "description": "width of image",
        "type": "number",
        "exclusiveMinimum": 1
    },
    "image": {
        "description": "the image is converted to byte datatype",
        "type": "byte"
    }
    },
    "required": [ "height", "width", "image" ]
}
"""

schema_registry_url ={'url':'http://localhost:8081'}

schema_registry_client = SchemaRegistryClient(schema_registry_url)

json_serializer = JSONSerializer(schema_str,schema_registry_client,image_to_dict)

conf = {'bootstrap.servers': 'localhost:9092',
            'key.serializer':StringSerializer('utf_8'),
            'value.serializer':json_serializer
        }

procedure = SerializingProducer(conf)

image_path = sys.argv[1]
topic = sys.argv[2]
image = cv2.imread(image_path)

_, buffer = cv2.imencode(os.path.split(os.path.basename(image_path))[1],image)

image_object =Image_Type(
    height = image.shape[0],
    width = image.shape[1],
    image =  buffer.tobytes()
)

procedure.produce(topic,key=str(uuid4()),value=image_object,on_delivery=delivery_report)


