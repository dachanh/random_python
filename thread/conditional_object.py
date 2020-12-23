import threading
import time 
import logging 



def thread_consumer(cv):
    with cv:
        cv.wait()


def thread_producer(cv):
    with cv:
        cv.notifyAll()

if __name__ == "__main__":
    condition = threading.Condition()
    consumer_1 =  threading.Thread(name = 'consumer 1',target=thread_consumer,args=(condition,))
    consumer_2 = threading.Thread(name='consumer 2',target=thread_consumer,args=(condition,))
    producer = threading.Thread(name='producer',target=thread_producer,args=(condition,))

    consumer_1.start()
    time.sleep()