import os
import cv2
import sys
import json
import numpy as np
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

topic =sys.argv[1]
def image_to_dict(data,ctx):
    return dict(
        height = data.height,
        width = data.width,
        image = data.image,
        extension = data.extension
    )



class Image_Type(object):
    def __init__(self,height,width,image ,extension):
        self.height = height 
        self.width = width
        self.image = image
        self.extension = extension



def delivery_report(err, msg):
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

schema_registry_url ={'url':'http://localhost:8082'}

schema_registry_client = SchemaRegistryClient(schema_registry_url)

json_serializer = JSONSerializer(schema_str,schema_registry_client,image_to_dict)

conf = {
            'bootstrap.servers': 'localhost:9092',
            'key.serializer':StringSerializer('utf_8'),
            'value.serializer':json_serializer
        }

procedure = SerializingProducer(conf)

app = Flask(__name__)
api = Api(app)

class recieve_image(Resource):
    def post(self):
        file = request.files['file']
        test_file = './temp.jpg'
        file.save(test_file)
        img = cv2.imread(test_file)
        _,buff = cv2.imencode( os.path.splitext(file.filename)[1],img)
        buff = buff.tobytes()
        print(buff)
        print(type(buff))
        # stream = file.stream.read()
        extension =  os.path.splitext(file.filename)[1]
        image_object =Image_Type(
                height = 7,
                width = 6,
                image =np.asarray(buff),
                extension =  extension
            )
        procedure.produce(topic,key=str(uuid4()),value=image_object,on_delivery=delivery_report)
        procedure.flush()
        return {"sds":"sd"},200

api.add_resource(recieve_image,'/')


if __name__ == "__main__":
    app.run('0.0.0.0',port=8176)



