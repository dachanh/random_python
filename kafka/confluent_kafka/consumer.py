import os
import cv2
import sys 
import logging
from io import BytesIO
import confluent_kafka
from threading import Thread
from confluent_kafka import Consumer ,KafkaException





conf = {
    'bootstrap.servers':'localhost:9092' ,
    'auto.offset.reset':'earliest' ,
    'group.id':'test-id',
    'session.timeout.ms':6000
}

logger = logging.getLogger('consumer')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(handler)


consumer = Consumer(conf, logger=logger)



try :
    while True:
        message =  consumer.poll(timeout=0.1)
        if message is None:
            continue
        if message.error():
            raise KafkaException(message.error())
        else:
            stream = BytesIO(message)