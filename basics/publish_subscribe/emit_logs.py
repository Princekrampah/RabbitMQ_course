import pika  # Import the Pika library to interact with RabbitMQ.
import sys   # Import sys to handle command-line arguments.

# Establish a connection to the RabbitMQ server running on the local machine.
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()  # Create a channel for communication with RabbitMQ.

# Declare a fanout exchange named 'logs'. A fanout exchange broadcasts messages to all queues that are bound to it.
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Concatenate all command-line arguments into a single string, which will be the message to send.
message = ' '.join(sys.argv[1:])

# Check if the message is empty. If no message is provided, print an error message and exit the program.
if message == "":
    print("No message provided")
    sys.exit(1)

# Publish the message to the 'logs' exchange. Since this is a fanout exchange, the routing_key is ignored.
# Hence no need to specify a routing_key.
channel.basic_publish(exchange='logs', routing_key='', body=message)

# Print a confirmation that the message has been sent.
print(f" [x] Sent {message}")

# Close the connection to RabbitMQ after the message is sent.
connection.close()