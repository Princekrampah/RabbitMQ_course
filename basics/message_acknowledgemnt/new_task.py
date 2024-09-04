import pika  # Import the pika library, which provides the tools needed to interact with RabbitMQ
import sys   # Import sys for handling command-line arguments

# Establish a connection to the RabbitMQ server running on localhost.
# BlockingConnection establishes a synchronous connection to RabbitMQ.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# Create a channel within the connection.
# Channels are virtual connections inside a connection to RabbitMQ.
channel = connection.channel()

# Declare a queue named 'hello'.
# Declaring a queue is idempotent ‒ it will only be created if it doesn't exist already.
channel.queue_declare(queue='hello')

# Join the command-line arguments into a single string, with spaces separating each argument.
# sys.argv[1:] takes all arguments except the script name.
# If no arguments are provided, the message will be an empty string.
message = ' '.join(sys.argv[1:]) or ""

# Check if the message is empty. If no message was provided, print an error and exit.
if message == "":
    print("No message provided")
    sys.exit(1)  # Exit the script with a status code of 1 to indicate an error.

# Publish the message to the 'hello' queue.
# The exchange is left as an empty string, which means the default exchange is used.
# The routing_key is set to 'hello', which is the name of the queue.
# The message content is passed as the 'body'.
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)

# Print a confirmation message to the console indicating that the message was sent.
print(f" [x] Sent {message}")

# Close the connection to RabbitMQ to ensure that any remaining messages in the buffer
# are sent and that the connection is properly closed.
connection.close()
