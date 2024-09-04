import pika

# Establish a connection to RabbitMQ on the local machine.
# pika.BlockingConnection establishes a synchronous connection to RabbitMQ.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# Create a channel within the connection. The channel is the medium 
# through which you communicate with RabbitMQ. The channel is where you define
# your message queues, publish messages, and consume messages. In this case, we'll 
# only publish messages.
channel = connection.channel()

# Declare a queue named 'hello'. If the queue doesn't exist, RabbitMQ 
# will create it for you. If it already exists, nothing happens.
# This is useful because you don't need to worry whether the queue 
# exists before trying to use it.
channel.queue_declare(queue='hello')


# RabbitMQ messages must always go through an exchange.
# An exchange is responsible for receiving messages from the producer 
# and pushing them to queues.
# There are different types of exchanges, but in this example, 
# we're using the default exchange, which is identified by an empty string.
# The default exchange is a direct exchange that routes messages to the queue 
# whose name exactly matches the routing_key.

# Publishing a message to the queue 'hello'.
# exchange='' means we're using the default exchange.
# routing_key='hello' specifies the queue that will receive the message.
# body='Hello World!' is the actual message content being sent to the queue.
channel.basic_publish(
    exchange='',
    routing_key='hello',
    body='Hello World!'
)

# Print a confirmation message to the console.
print(" [x] Sent 'Hello World!'")

# Flush the message buffer to ensure all messages are sent out 
# before closing the connection. This is important because if you close 
# the connection before all messages are sent, some messages might be lost.
# Finally, close the connection to RabbitMQ.
connection.close()
