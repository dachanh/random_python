import os
import cv2
import sys 
import logging
import tempfile
import numpy as np
import confluent_kafka
from PIL import Image
from io import BytesIO
from shutil import copy2 as cp 
from threading import Thread
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka.serialization import StringDeserializer



class Image_Type(object):
    def __init__(self,height,width,image ,extension):
        self.height = height 
        self.width = width
        self.image = image
        self.extension = extension


def dict_to_image(obj,ctx):

    if obj is None:
        return None 
    return Image_Type(height = obj['height'],
                        width =  obj['width'],
                            image=obj['image'],
                            extension = obj['extension']) 



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
        "type": "number",
        "exclusiveMinimum": 1
    },
    "width": {
        "description": "width of image",
        "type": "number",
        "exclusiveMinimum": 1
    },
    "image": {
        "description": "the image is converted to byte datatype",
        "type": "array"
    },
    "extension": {
        "description": "",
        "type" : "string"
    }
    },
    "required": [ "height", "width", "image" ,"extension"]
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

while True:
    message =  consumer.poll(timeout=0.0001)
    if message is None:
        continue
    if message.error():
        raise KafkaException(message.error())
    else:
        req = message.value()
        print(req.image)
        # print(req.image.encode())
        # print(type(req.image.encode()))
        # req.image =  BytesIO(req.image.encode())
        # print(req.image)
        # print(type(req.image))
        # print(req.image.read())
        # data = np.load(req.image,allow_pickle=True)
        # print(data)
        # with open('temp.jpg','wb') as f:
        #     f.write(req.image.getbuffer())
        # file_bytes = np.asarray(bytearray(req.image.getbuffer()), dtype=np.uint8)
        # img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        # print(img.shape)
        # temp = tempfile.NamedTemporaryFile(mode='wb' , prefix="tmp_",suffix=req.extension, delete=True)
        # with temp as write_tmp:
        #     write_tmp.write(req.image.getbuffer())
        #     cp(write_tmp.name,'./')
consumer.close()