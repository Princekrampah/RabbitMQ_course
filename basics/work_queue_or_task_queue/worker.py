import pika
import sys
import os
import time

# Main function that sets up the connection and consumer
def main():
    # Establish a connection to the RabbitMQ server running on localhost.
    # pika.BlockingConnection is used to create a blocking (synchronous) connection.
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    
    # Create a channel within the connection.
    # The channel is where you define your message queues, publish messages, and consume messages.
    channel = connection.channel()

    # Declare a queue named 'hello'.
    # Declaring the queue ensures that it exists before attempting to use it.
    # If the queue already exists, this declaration does nothing.
    channel.queue_declare(queue='hello')

    # Define a callback function that will be called whenever a message is received.
    # This function processes the message and simulates some work by sleeping for
    # a number of seconds equal to the number of dots in the message.
    def callback(ch, method, properties, body):
        # Print the received message, decoding it from bytes to a string.
        print(f" [x] Received {body.decode()}")
        
        # Simulate a time-consuming task by sleeping for a number of seconds
        # equal to the number of dots in the message.
        time.sleep(body.count(b'.'))
        
        # Print a message indicating that the processing is done.
        print(" [x] Done")

    # The default behavior of RabbitMQ is to distribute messages evenly among consumers.
    # This is called round-robin distribution. It means that if you have multiple consumers
    # listening on the same queue, RabbitMQ will send each new message to the next consumer in line.
    # 
    # The 'auto_ack=True' setting means that messages are acknowledged automatically as soon
    # as they are received, which tells RabbitMQ that the message has been successfully processed.
    # The 'on_message_callback=callback' specifies the function to call when a message is received.
    channel.basic_consume(queue='hello',
                          auto_ack=True,
                          on_message_callback=callback)

    # Print a message to indicate that the consumer is waiting for messages.
    print(' [*] Waiting for messages. To exit press CTRL+C')

    # Start consuming messages from the queue.
    # This is a blocking call that will keep the script running, waiting for messages to process.
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
