import sys
import pika

conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = conn.channel()


message = ' '.join(sys.argv[1:]) or "hello world"

channel.queue_declare(queue='hello')



channel.basic_publish(exchange="",
			routing_key="hello",
				body=message)
print("[x] Send ",message)
conn.close()



