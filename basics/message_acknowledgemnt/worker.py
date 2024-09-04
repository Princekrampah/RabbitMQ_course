import pika  # Import the pika library to interact with RabbitMQ
import sys   # Import sys for handling system-level operations like exiting the program
import os    # Import os for lower-level system operations
import time  # Import time for adding delays in processing


def main():
    # Establish a connection to the RabbitMQ server running on localhost.
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))

    # Create a channel within the connection.
    channel = connection.channel()

    # Declare a queue named 'hello'. If the queue already exists, this operation has no effect.
    channel.queue_declare(queue='hello')

    # define callback
    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        # send an acknowledgment aka ack to let the consumer know
        # that the message has been received, processed and can be
        # removed from the queue.

        # If not acknowledged, the message will be requeued and sent
        # to another consumer. This way, if a consumer dies, the message
        # will not be lost but will be sent to another consumer. Hence,
        # the message will be processed and not lost.

        # By default the timeout for the acknowledgment is 30 minutes.
        # The timeout can be changed by setting the heartbeat parameter

        # This way even if the consumer dies, while processing the message,
        # the message will be sent to another consumer and will be processed.

        # All acknowledgments are sent on the same channel that received the
        # delivery. It's important to note that acknowledgments are not sent on a
        # separate channel. This will lead to a channel-level protocol exception.

        # Failure to acknowledge a message can lead to messages being redelivered
        # over and over again to the consumer. This is why it's important to handle
        # the acknowledgment process properly. The more the message is redelivered,
        # the more memory and CPU will be used. As it won't be able to release any unacknowledged messages.
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Set up the consumer with manual acknowledgment (auto_ack=False).
    # The callback function will be called whenever a message is received.
    channel.basic_consume(queue='hello', on_message_callback=callback)

    # Print a message to indicate that the consumer is ready and waiting for messages.
    print(' [*] Waiting for messages. To exit press CTRL+C')

    # Start consuming messages. This function will keep the script running, waiting for messages.
    channel.start_consuming()


# The entry point of the script.
if __name__ == '__main__':
    try:
        main()  # Run the main function
    except KeyboardInterrupt:
        # Handle the situation where the user presses CTRL+C to exit the script.
        print('Interrupted')
        try:
            sys.exit(0)  # Exit the program cleanly
        except SystemExit:
            os._exit(0)  # Force exit the program if sys.exit fails
