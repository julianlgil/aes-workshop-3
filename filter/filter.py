import pika
import time
import os

# read rabbitmq connection url from environment variable
amqp_url = os.environ['AMQP_URL']
# from pdb import set_trace; set_trace()

url_params = pika.URLParameters(amqp_url)

# connect to rabbitmq
connection = pika.BlockingConnection(url_params)
connection_filtered = pika.BlockingConnection(url_params)
chan = connection.channel()

# declare a new queue
# durable flag is set so that messages are retained
# in the rabbitmq volume even between restarts
chan.queue_declare(queue='messages', durable=True)
chan.queue_declare(queue='filtered-messages', durable=True)

def receive_msg(ch, method, properties, body):
    """function to receive the message from rabbitmq
    print it
    sleep for 2 seconds
    ack the message"""

    print('received msg from read-api : ', body.decode('utf-8'))
    chan.basic_publish(exchange='', routing_key='filtered-messages',
                       body='filtered message', properties=pika.BasicProperties(delivery_mode=2))
    time.sleep(2)
    ch.basic_ack(delivery_tag=method.delivery_tag)


# to make sure the consumer receives only one message at a time
# next message is received only after acking the previous one
chan.basic_qos(prefetch_count=1)

# define the queue consumption
chan.basic_consume(queue='messages',
                   on_message_callback=receive_msg)

print("Waiting to consume")
# start consuming
chan.start_consuming()