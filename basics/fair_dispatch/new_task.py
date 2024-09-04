#!/usr/bin/env python
# The shebang line specifies that the script should be run with the Python interpreter.

import pika  # Import the Pika library for connecting to RabbitMQ.
import sys  # Import the sys module to access command-line arguments.

# Establish a connection to the RabbitMQ server on the local machine.
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
# Create a new channel through which you can communicate with RabbitMQ.
channel = connection.channel()

# Declare a queue named 'task_queue'. The durable=True option ensures that the queue will survive a RabbitMQ restart.
channel.queue_declare(queue='task_queue', durable=True)

# Combine all command-line arguments into a single string, separated by spaces.
message = ' '.join(sys.argv[1:])

# If no message was provided (i.e., the string is empty), print a warning and exit the program.
if message == "":
    print("No message provided")
    sys.exit(1)

# Publish the message to the 'task_queue' queue.
# The empty string for exchange means that we're using the default exchange.
# The routing_key is set to 'task_queue' to specify the destination queue.
# The message is marked as persistent with delivery_mode=pika.DeliveryMode.Persistent,
# ensuring it won't be lost if RabbitMQ crashes.
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent
    )
)

# Print a confirmation that the message has been sent.
print(f" [x] Sent {message}")

# Close the connection to RabbitMQ to free up resources.
connection.close()