#!/usr/bin/env python
# The shebang line tells the operating system to run this script with the Python interpreter.

import pika  # Import the Pika library, which is used to interact with RabbitMQ.
import time  # Import the time module for adding delays in message processing.

# Establish a connection to RabbitMQ server running on localhost.
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()  # Create a new channel (session) with RabbitMQ.

# Declare a queue named 'task_queue' that will be used to store tasks. 
# The durable=True option ensures that the queue survives server restarts.
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')  # Notify that the worker is ready and waiting for messages.

# Callback function that is triggered when a message is received from the queue.
def callback(ch, method, properties, body):
    # Print the received message body after decoding it from bytes to string.
    print(f" [x] Received {body.decode()}")
    
    # Simulate processing time by sleeping for a number of seconds equal to the count of '.' in the message.
    time.sleep(body.count(b'.'))
    
    # After processing the message, print 'Done' and acknowledge the message.
    # This tells RabbitMQ that the message has been processed and can be removed from the queue.
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Set the Quality of Service (QoS) settings for the channel.
# prefetch_count=1 ensures that a worker is only sent one message at a time, 
# and won't receive another until it has acknowledged the previous one.
channel.basic_qos(prefetch_count=1)

# Tell RabbitMQ that this worker should listen to the 'task_queue' queue, 
# and when a message is received, the callback function should be called to process it.
channel.basic_consume(queue='task_queue', on_message_callback=callback)

# Start consuming messages from the queue. This is a blocking call that keeps the script running.
channel.start_consuming()
