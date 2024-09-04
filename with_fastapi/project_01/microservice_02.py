import pika
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
RABBITMQ_URL = os.environ.get("RABBITMQ_URL")


def main():
    # rabbitmq connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_URL))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(
        queue='hello',
        auto_ack=True,
        on_message_callback=callback
    )

    channel.basic_consume(
        queue="hello", on_message_callback=callback
    )

    print("Waiting for messages. To exit press CTRL+C...")

    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
