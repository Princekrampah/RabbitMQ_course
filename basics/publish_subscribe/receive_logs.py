import pika  # Import the Pika library to interact with RabbitMQ.

# Establish a connection to the RabbitMQ server running on the local machine.
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()  # Create a channel for communication with RabbitMQ.

# Declare a fanout exchange named 'logs'. A fanout exchange broadcasts messages to all queues that are bound to it.
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Declare a new queue with a random name. The queue is exclusive, meaning it will be deleted when the consumer disconnects.
# The server assigns a random name to the queue (e.g., amq.gen-JzTY20BRgKO-HjmUJj0wLg).
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue  # Store the randomly generated queue name.

# Binding is a relationship between an exchange and a queue. 
# This can be simply read as: the queue is interested in messages from this exchange.
# Bind the newly created queue to the 'logs' exchange.
# A binding connects the exchange to the queue, allowing messages from the exchange to be delivered to the queue.
channel.queue_bind(exchange='logs', queue=queue_name)

# Print a message indicating that the script is waiting for logs to be received.
print(' [*] Waiting for logs. To exit press CTRL+C')


# Define a callback function that will be executed whenever a message is received from the queue.
# The function simply prints the received message to the console.
def callback(ch, method, properties, body):
    print(f" [x] {body}")

# Start consuming messages from the queue. The callback function will be called whenever a message is delivered.
# The auto_ack=True parameter means that the messages will be acknowledged immediately after being received.
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True
)

# Enter a blocking loop that waits for messages and invokes the callback function when a message is received.
channel.start_consuming()
