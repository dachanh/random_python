import os
import cv2
import sys 
import logging
import confluent_kafka
from PIL import Image
from io import BytesIO
from threading import Thread
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka.serialization import StringDeserializer



class Image_Type(object):
    def __init__(self,height,width,image):
        self.height = height 
        self.width = width
        self.image = image


def dict_to_image(obj,ctx):

    if obj is None:
        return None 
    return Image_Type(height = obj['height'],
                        width =  obj['width'],
                            image= obj['image']) 



topic_subcribe = sys.argv[1]

conf = {
    'bootstrap.servers':'localhost:9092' ,
    'auto.offset.reset':'earliest' ,
    'group.id':'test-id',
    'session.timeout.ms':6000
}


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


json_deserializer = JSONDeserializer(schema_str,
                                        from_dict=dict_to_image)

string_deserializer =  StringDeserializer('utf_8')

conf = {'bootstrap.servers':  'localhost:9092',
                     'key.deserializer': string_deserializer,
                     'value.deserializer': json_deserializer,
                     'group.id': 'test-json',
                     'auto.offset.reset': "earliest"}

consumer = DeserializingConsumer(conf)

consumer.subscribe([topic_subcribe])

try :
    while True:
        message =  consumer.poll(timeout=0.1)
        if message is None:
            continue
        if message.error():
            raise KafkaException(message.error())
        else:
            image_obj = message.value()
            print("height : "+str(image_obj.height)+", width : "+str(image_obj.width) )
            stream = BytesIO(image_obj.image) 
            image = Image.open(stream).convert("RGBA")
            cv2.imwrite("test.jpg",image)
            stream.close()
except Exception as e:
    print(e)
consumer.close()