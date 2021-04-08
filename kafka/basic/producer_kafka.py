import json
import threading
import queue
from time import sleep 
from kafka import KafkaProducer

class threadQueue(threading.Thread):
    def __init__(self,queue,producer,topic):
        threading.Thread.__init__(self)
        self.queue = queue
        self.producer = producer
        self.topic = topic
    def run(self):
        while True:
            data = self.queue.get()
            try:
                self.producer.send(self.topic,data)
            except Exception as e :
                print(e)
            self.queue.task_done()
producer  =KafkaProducer(bootstrap_servers = ['localhost:9092'],
                        value_serializer=lambda x: json.dumps(x).encode('utf-8'))
queue = queue.Queue()

task = [{'number': it } for it in range(1000)]
for i in range(1000):
    t = threadQueue(queue,producer,'test')
    t.setDaemon(True)
    t.start()

for it in task:
    queue.put(it)

try :
    queue.join()
except Exception as e :
    print(e)
