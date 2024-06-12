import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

message = ' '.join(sys.argv[1:]) or ""

if message == "":
    print("No message provided")
    sys.exit(1)

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)

print(f" [x] Sent {message}")
