import json
from kafka import KafkaConsumer 
from pymongo import MongoClient


consumer =  KafkaConsumer(
    'test',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

client = MongoClient('localhost:27017')
collection = client.numtest.numtest
for message in consumer:
    message = message.value
    print('{} added to {}'.format(message,collection))
