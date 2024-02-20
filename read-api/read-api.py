from utils.utils import RabbitMQ
import os
import Content.Token.access_token as access_token
import Content.Artist.access_artist as access_artist
import properties
import Content.Artist.random_year as random_year

if __name__ == '__main__':
    rabbit = RabbitMQ(amqp_url = os.environ['AMQP_URL'])

    token = access_token.get_token()
    for i in range(properties.random_year_quantity):
        year=random_year.random_year()
        artists = access_artist.search_for_artist(token, year,properties.limit)
        rabbit.publish('messages', str(artists))
    rabbit.close_connection()
