from typing import Union

from fastapi import FastAPI
from contextlib import asynccontextmanager

import pika

app = FastAPI()

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost"))
channel = connection.channel()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create queue
    channel.queue_declare(queue='hello')


@app.on_event("shutdown")
def shutdown_event():
    connection.close()


@app.get("/send_msg")
def read_item(msg: str):
    channel.basic_publish(
        exchange='',
        routing_key='hello',
        body=msg
    )

    print(f" [x] Sent {msg}")

    return {"msg": "msg sent to hello queue"}
