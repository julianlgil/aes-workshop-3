import pika

def publisher(channel, message):
    #print('Message preview')
    channel.basic_publish(exchange='',routing_key='test-msg', body=message)
    #print('Message send')


def open_connection():
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    # channel.queue_declare(queue='test-msg')
    # me    ssage = 'test message'
    #print("AAAAAAA")
    return connection,channel

def close_connection(connection):
    connection.close