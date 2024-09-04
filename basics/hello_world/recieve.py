import pika
import sys
import os

# Define the main function that sets up the consumer
def main():
    # Establish a connection to RabbitMQ server running on localhost.
    # pika.BlockingConnection establishes a synchronous connection.
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    
    # Create a channel within the connection.
    # The channel is where you define your message queues, publish messages, and consume messages.
    channel = connection.channel()

    # Declare a queue named 'hello'. If it already exists, RabbitMQ won't create it again.
    # It's a good practice to declare the queue in both the producer and consumer 
    # to ensure that the queue exists when either script runs.
    channel.queue_declare(queue='hello')

    # Define a callback function that will be called whenever a message is received.
    # The 'body' parameter contains the message content.
    # ch (channel) ‒ the channel object; method ‒ method frame with delivery tag, etc.
    # properties ‒ message properties (like content type, headers, etc.)
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    # Tell RabbitMQ that this callback function should receive messages from the 'hello' queue.
    # auto_ack=True automatically acknowledges that the message has been received.
    # If auto_ack is set to False, the consumer must acknowledge the message manually, 
    # which can be useful for ensuring that messages aren't lost if a consumer crashes.
    channel.basic_consume(
        queue='hello',            # Name of the queue to consume from
        auto_ack=True,            # Automatically acknowledge the message receipt
        on_message_callback=callback  # The function to call when a message is received
    )

    # Print a message to the console to indicate that the consumer is waiting for messages.
    print(' [*] Waiting for messages. To exit press CTRL+C')

    # Start consuming messages. This will keep the script running, waiting for messages 
    # to arrive and processing them with the callback function.
    channel.start_consuming()

# Check if the script is being run directly (not imported as a module)
if __name__ == '__main__':
    try:
        main()  # Run the main function
    except KeyboardInterrupt:  # Catch the interrupt signal (Ctrl+C) to stop the consumer
        print('Interrupted')
        try:
            sys.exit(0)  # Exit the script cleanly
        except SystemExit:
            os._exit(0)  # Forcefully exit if sys.exit fails
