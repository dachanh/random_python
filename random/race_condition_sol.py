import os
import logging
import threading
import time

x = 0
def increment():
   global x
   x +=1



def function_statement(lock):
  lock.acquire()
  global x
  for _ in range(50000):
    increment()
  print(threading.current_thread().name,' ',x)
  lock.release()
def run_thread():
   lock = threading.Lock()
   thread1 = threading.Thread(target=function_statement,args=(lock,))
   thread2 = threading.Thread(target=function_statement,args=(lock,))
   thread1.start()
   thread2.start()
   thread1.join()
   thread2.join()


if __name__ == "__main__":
  for _ in range(2):
     run_thread()
