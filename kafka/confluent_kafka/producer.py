import os
import cv2
import sys 
import confluent_kafka
from threading import Thread
from confluent_kafka import Producer




image_path = sys.argv[1]
image = cv2.imread(image_path)

_, buffer = cv2.imencode

conf = {'bootstrap.servers': "localhost:9092"}


procedure = Producer(**conf)

data = {
    'height': image.shape[0] ,
    'width': image.shape[1] ,
    'data': buffer.tobytes()
}




procedure.send("test-transfer-image",)