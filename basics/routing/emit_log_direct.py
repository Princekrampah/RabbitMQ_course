import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# We were using a fanout exchange, which doesn't give us too much flexibility -
# it's only capable of mindless broadcasting.

# We will use a direct exchange instead. The routing algorithm behind a direct exchange
# is simple - a message goes to the queues whose binding key exactly matches the
# routing key of the message.
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'

message = ' '.join(sys.argv[1:])

if message == "":
    print("No message provided")
    sys.exit(1)

channel.basic_publish(
    exchange='direct_logs', routing_key=severity, body=message)

print(f" [x] Sent {severity}:{message}")

connection.close()
