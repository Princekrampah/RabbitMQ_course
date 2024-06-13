import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# declare a fanout exchange
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# create a queue with a random name, allow the server to delete it 
# once the consumer connection is closed. Secondly, once the consumer 
# connection is closed, the queue should be deleted. 
# There's an exclusive flag for that:
# example: amq.gen-JzTY20BRgKO-HjmUJj0wLg
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# connect the queue to the exchange
# We've already created a fanout exchange and a queue. 
# Now we need to tell the exchange to send messages to our queue. 
# That relationship between exchange and a queue is called a binding.
channel.queue_bind(exchange='logs', queue=queue_name)
# From now on the logs exchange will append messages to our queue.


# You can list existing bindings using, you guessed it,

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {body}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
