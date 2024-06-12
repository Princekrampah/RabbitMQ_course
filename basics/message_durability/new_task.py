import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


# Although this command is correct by itself, it won't work in our
# setup. That's because we've already defined a queue called hello
# which is not durable. RabbitMQ doesn't allow you to redefine an
# existing queue with different parameters and will return an error
# to any program that tries to do that. But there is a quick
# workaround - let's declare a queue with different name, for
# example task_queue:
channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or ""

if message == "":
    print("No message provided")
    sys.exit(1)


# This queue_declare change needs to be applied to both the producer and consumer code.
# At that point we're sure that the task_queue queue won't be lost even if RabbitMQ 
# restarts. Now we need to mark our messages as persistent - by supplying a delivery_mode 
# property with the value of pika.DeliveryMode.Persistent
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=pika.DeliveryMode.Persistent
                      ))

print(f" [x] Sent {message}")
