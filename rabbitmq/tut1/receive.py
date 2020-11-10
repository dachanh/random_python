import pika , sys , os


def main():
  conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
  channel = conn.channel()
  channel.queue_declare(queue='hello')
  def callback(ch,method,properties,body):
    print("[x] Received %r" % body)
  channel.basic_consume(queue='hello',on_message_callback=callback,auto_ack=True)
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
