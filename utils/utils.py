import pika
import time
import os


class RabbitMQ:
    def __init__(self, amqp_url) -> None:
        url_params = pika.URLParameters(amqp_url)
        self.connection = pika.BlockingConnection(url_params)
        self.chan = self.connection.channel()

    def publish(self, queue, message) -> None:
        self.chan.queue_declare(queue=queue, durable=True)
        self.chan.basic_publish(exchange='', routing_key=queue,
                                body=message, properties=pika.BasicProperties(delivery_mode=2))

    def subscribe(self, queue, callback) -> None:
        self.chan.queue_declare(queue=queue, durable=True)
        self.chan.basic_qos(prefetch_count=1)
        self.chan.basic_consume(queue=queue, on_message_callback=callback)
        print("Waiting to consume ", queue)
        self.chan.start_consuming()

    def close_connection(self) -> None:
        self.chan.close()
        self.connection.close()


class CallBack:
    def __init__(self, rabbit) -> None:
        self.rabbit = rabbit

    def cb(self, ch, method, properties, body):
        """function to receive the message from rabbitmq
        print it
        sleep for 2 seconds
        ack the message"""

        print('received msg from read-api : ', body.decode('utf-8'))
        self.rabbit.publish('filtered-messages', 'this is the message')
        time.sleep(2)
        ch.basic_ack(delivery_tag=method.delivery_tag)
