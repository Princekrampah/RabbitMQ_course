## Message Acknowledgement Duration

We’ve learned how to keep tasks safe even if the consumer crashes. But if the RabbitMQ server itself stops, our tasks could still be lost.

When RabbitMQ shuts down or fails, it forgets the queues and messages unless we tell it not to. To avoid losing messages, we need to make both the queue and messages durable.

First, to ensure the queue survives a RabbitMQ restart, we should declare it as durable:

