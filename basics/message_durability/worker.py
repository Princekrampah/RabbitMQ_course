import pika  # Import the pika library for interacting with RabbitMQ
import sys   # Import sys for handling command-line arguments and exiting the program
import os    # Import os to handle system-level operations like exiting the script
import time  # Import time to simulate work by adding delays


def main():
    # Establish a connection to the RabbitMQ server running on localhost
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue as durable to ensure it survives a RabbitMQ restart.
    channel.queue_declare(queue='task_queue', durable=True)

    # Define a callback function to process received messages.
    def callback(ch, method, properties, body):
        # Decode and print the received message
        print(f" [x] Received {body.decode()}")
        # Simulate work by sleeping for 1 second per '.' in the message
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        # Send an acknowledgment (ack) to RabbitMQ to confirm that the message has been processed.
        # Without this ack, the message will be requeued and sent to another consumer.
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Consume messages from the 'task_queue'.
    # We do not set auto_ack=True because we want to manually acknowledge the message after processing.
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()  # Start the consumer loop


if __name__ == '__main__':
    try:
        main()  # Run the main function
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)  # Gracefully exit the program
        except SystemExit:
            os._exit(0)  # Forcefully exit the program if needed
