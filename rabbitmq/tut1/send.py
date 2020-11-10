import pika

conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = conn.channel()


channel.queue_declare(queue='hello')

channel.basic_publish(exchange="",
			routing_key="hello",
				body="hello world thanh")
print("[x] Send 'hello world'")
conn.close()



