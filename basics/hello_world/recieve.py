import pika
import sys
import os


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # we can run this as many times as we want by only one will be created

    # You may ask why we declare the queue again ‒ we have already declared
    # it in our previous code. We could avoid that if we were sure that the
    # queue already exists. For example if send.py program was run before.
    # But we're not yet sure which program to run first. In such cases it's
    # a good practice to repeat declaring the queue in both programs.
    channel.queue_declare(queue='hello')

    # define callback
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='hello',
                          auto_ack=True,
                          on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
