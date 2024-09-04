#!/usr/bin/env python
import pika  # Import the Pika library for RabbitMQ interaction.
import sys   # Import sys to handle command-line arguments.

# Establish a connection to the RabbitMQ server running on localhost.
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()  # Create a channel for communication with RabbitMQ.

# Declare a direct exchange named 'direct_logs'. A direct exchange routes messages
# to queues based on an exact match between the message's routing key and the queue's binding key.
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# Declare a queue with a unique name. This queue will be exclusive to this connection
# and will be deleted when the connection is closed. The result.method.queue gives
# us the name of the created queue.
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Get the severities (routing keys) from command-line arguments.
# Severities are used to specify which types of messages this queue is interested in.
severities = sys.argv[1:]

# If no severities are provided, print usage instructions and exit.
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

# Bind the queue to the 'direct_logs' exchange for each severity provided.
# This tells RabbitMQ that the queue should receive messages from the exchange
# with the specified routing keys.
for severity in severities:
    channel.queue_bind(
        exchange='direct_logs', queue=queue_name, routing_key=severity
    )
    # Multiple bindings can be created for the same queue with different routing keys.
    # If multiple queues are bound to the same routing key, messages with that key
    # will be delivered to all matching queues.

# Print a message indicating that the script is waiting for logs.
# To stop the script, press CTRL+C.
print(' [*] Waiting for logs. To exit press CTRL+C')

# Define a callback function to handle incoming messages.
# This function is called when a message is delivered to the queue.
def callback(ch, method, properties, body):
    # Print the message body along with the routing key that the message was sent with.
    print(f" [x] {method.routing_key}:{body.decode()}")

# Set up the consumer to use the callback function defined above.
# Auto-acknowledgment is enabled, meaning messages will be removed from the queue
# as soon as they are delivered to the callback function.
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True
)

# Start consuming messages from the queue. This method will run indefinitely,
# processing messages as they arrive.
channel.start_consuming()