import pika
import sys
import os
import time
"""
message acknowledgments
if the consumer die  message acknowledgemnt will
send back the message to queue (re-queue it)

"""


def main():
  conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
  channel = conn.channel()
  channel.queue_declare(queue='hello')
  def callback(ch,method,properties,body):
    print("[x] Received ",body.decode())
    print(body.count(b'.'))
    time.sleep(body.count(b'.'))
    print("[x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)
  channel.basic_consume(queue='hello',on_message_callback=callback)
  print(' [*] Waiting for messages')
  channel.start_consuming()


if __name__ == '__main__':
  try:
     main()
  except  KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except:
               os._exit(0)
