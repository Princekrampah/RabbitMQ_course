import pika
import sys

# Establish a connection to the RabbitMQ server running on localhost.
# pika.BlockingConnection establishes a synchronous connection.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# Create a channel within the connection. The channel is where you define
# your message queues, publish messages, and consume messages.
channel = connection.channel()

# Declare a queue named 'hello'. If it already exists, RabbitMQ won't create it again.
# Declaring a queue is a way of ensuring that the queue you want to publish to or consume
# from exists before you try to use it.
channel.queue_declare(queue='hello')

# Join the command-line arguments (sys.argv[1:]) into a single string separated by spaces.
# If no command-line arguments are provided, the message will be an empty string.
message = ' '.join(sys.argv[1:]) or ""

# Check if the message is empty. If no message was provided via the command line,
# print an error message and exit the program with a non-zero status code, indicating an error.
if message == "":
    print("No message provided")
    sys.exit(1)

# Publish the message to the 'hello' queue.
# exchange='' means we're using the default exchange, which routes messages directly
# to the queue specified by the routing_key.
# routing_key='hello' specifies the queue that will receive the message.
# body=message is the actual content of the message being sent.
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)

# Print a confirmation message to the console indicating that the message was sent.
print(f" [x] Sent {message}")

# Close the connection to RabbitMQ.
# This ensures that any remaining messages in the buffer are sent before the connection is closed.
connection.close()
