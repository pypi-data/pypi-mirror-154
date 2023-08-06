from typing import Callable

import pika
from os import environ
from abc import ABC


class RabbitMQWrapper(ABC):
    _connection = None
    _channel = None
    exchange = None

    def __init__(self, host: str = None, port: int = None, user: str = None, password: str = None) -> None:
        self._host = host or environ.get('RABBITMQ_HOST')
        self._port = port or environ.get('RABBITMQ_PORT')
        self._username = user or environ.get('RABBITMQ_USER')
        self._password = password or environ.get('RABBITMQ_PASSWORD')
        self.connect()

    def connect(self) -> None:
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self._host,
                port=self._port,
                credentials=pika.PlainCredentials(
                    username=self._username,
                    password=self._password
                )
            )
        )
        self._channel = self._connection.channel()


class RabbitMQPub(RabbitMQWrapper):

    def __init__(self, host: str = None, port: int = None, user: str = None, password: str = None) -> None:
        super().__init__(host=host, port=port, user=user, password=password)

    def set_exchange(self, name: str, ex_type: str = 'direct') -> None:
        self.exchange = name
        self._channel.exchange_declare(
            exchange=name, exchange_type=ex_type
        )

    def publish(self, msg, routing_key) -> None:
        self._channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=msg
        )


def callback(ch, method, properties, body):
    print(f'ch: {ch}')
    print(f'method: {method}')
    print(f'properties: {properties}')
    print(f'body: {body}')


class RabbitMQSub(RabbitMQWrapper):
    _callback: Callable = callback
    _queue = None

    def __init__(self, host: str = None, port: int = None, user: str = None, password: str = None) -> None:
        super().__init__(host=host, port=port, user=user, password=password)

    def set_callback(self, func: Callable) -> None:
        self._callback = func

    def set_queue(self, exchange_name: str, queue_name: str, routing_key: str):
        self._queue = self._channel.queue_declare(queue_name)
        self._channel.queue_bind(
            exchange=exchange_name,
            queue=queue_name,
            routing_key=routing_key
        )

    def run(self):
        self._channel.basic_consume(
            on_message_callback=self._callback,
            queue=self._queue.method.queue
        )
