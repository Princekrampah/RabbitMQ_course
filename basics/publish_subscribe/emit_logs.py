import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# declare a fanout exchange
channel.exchange_declare(exchange='logs', exchange_type='fanout')


message = ' '.join(sys.argv[1:])

if message == "":
    print("No message provided")
    sys.exit(1)

# The exchange parameter is the name of the exchange. The empty
# string denotes the default or nameless exchange: messages are
# routed to the queue with the name specified by routing_key, if
# it exists.
channel.basic_publish(exchange='logs', routing_key='', body=message)
# The producer program, which emits log messages, doesn't look much
# different from the previous tutorial. The most important change is
# that we now want to publish messages to our logs exchange instead
# of the nameless one. We need to supply a routing_key when sending,
# but its value is ignored for fanout exchanges.

print(f" [x] Sent {message}")

connection.close()
