import pika  # Import the pika library for interacting with RabbitMQ
import sys   # Import sys for handling command-line arguments and exiting the program

# Establish a connection to the RabbitMQ server running on localhost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a durable queue named 'task_queue'.
# Note: If a queue with the same name already exists but isn't marked as durable,
# RabbitMQ will throw an error. This is because you can't change a queue's properties
# after it's been created. To avoid this issue, we declare a new queue with a unique name.
channel.queue_declare(queue='task_queue', durable=True)

# Construct the message to be sent. It takes any command-line arguments provided.
# If no arguments are provided, it defaults to an empty string.
message = ' '.join(sys.argv[1:]) or ""

# If no message was provided via command-line arguments, print an error and exit.
if message == "":
    print("No message provided")
    sys.exit(1)

# Send the message to the 'task_queue'. The message is made persistent by setting
# the delivery_mode property to pika.DeliveryMode.Persistent. This ensures that
# the message won't be lost even if RabbitMQ restarts.
channel.basic_publish(
    exchange='',  # Use the default exchange
    routing_key='task_queue',  # Send the message to the 'task_queue'
    body=message,  # The actual message to be sent
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent  # Mark the message as persistent
    )
)

# Print a confirmation message to the console indicating that the message was sent.
print(f" [x] Sent {message}")