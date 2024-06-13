#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]

if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    # A binding is a relationship between an exchange and a queue. This can be
    # simply read as: the queue is interested in messages from this exchange.
    channel.queue_bind(
        exchange='direct_logs', queue=queue_name, routing_key=severity)
    # It is perfectly legal to bind multiple queues with the same binding key.
    # In our example we could add a binding between X and Q1 with binding key black.
    # In that case, the direct exchange will behave like fanout and will broadcast
    # the message to all the matching queues. A message with routing key black will
    # be delivered to both Q1 and Q2.

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
