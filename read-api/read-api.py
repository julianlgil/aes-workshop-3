import json

from utils.utils import RabbitMQ
import os
import content.token.access_token as access_token
import content.artist.access_artist as access_artist
import properties
import content.artist.random_year as random_year

if __name__ == '__main__':
    rabbit = RabbitMQ(amqp_url=os.environ['AMQP_URL'])
    queue_name = os.getenv('INITIAL_QUEUE_NAME')
    token = access_token.get_token()
    for i in range(properties.random_year_quantity):
        year = random_year.random_year()
        artists = access_artist.search_for_artist(token, year, properties.limit)
        rabbit.publish(queue_name, json.dumps(artists))
    rabbit.close_connection()
