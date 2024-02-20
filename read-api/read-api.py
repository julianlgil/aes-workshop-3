from utils.utils import RabbitMQ
import os

if __name__ == '__main__':
    rabbit = RabbitMQ(amqp_url = os.environ['AMQP_URL'])

    # publish a 100 messages to the queue
    for i in range(5):
        rabbit.publish('messages', 'Hola ¿Todo bien?')
