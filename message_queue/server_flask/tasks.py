import time 
import random 
import os 
from server_flask.extensions import celery

@celery.task(name="tasks.add")
def add(a,b):
    resp = {
        'id': add.request.id,
        'result': None
    }
    sleep_for = 0.2
    print("Going to sleep for {} seconds...".format(sleep_for))
    time.sleep(sleep_for)
    a = int(a)
    b = int(b)
    resp['result'] = a + b
    return resp