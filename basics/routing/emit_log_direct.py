import pika  # Import the Pika library to interact with RabbitMQ.
import sys   # Import sys to handle command-line arguments.

# Establish a connection to the RabbitMQ server running on the local machine.
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()  # Create a channel for communication with RabbitMQ.

# Declare a direct exchange named 'direct_logs'. A direct exchange routes messages
# to queues based on an exact match between the routing key of the message and
# the binding key of the queue.
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# Get the severity level from the command-line arguments, defaulting to 'info'
# if no argument is provided. The severity will be used as the routing key.
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'

# Concatenate all command-line arguments (excluding the severity) into a single string for the message.
message = ' '.join(sys.argv[2:])

# Check if the message is empty. If no message is provided, print an error message and exit the program.
if message == "":
    print("No message provided")
    sys.exit(1)

# Publish the message to the 'direct_logs' exchange. The message is routed to the queue(s)
# whose binding key exactly matches the severity.
channel.basic_publish(
    exchange='direct_logs', routing_key=severity, body=message
)

# Print a confirmation that the message has been sent, including the severity level and the message.
print(f" [x] Sent {severity}:{message}")

# Close the connection to RabbitMQ after the message is sent.
connection.close()