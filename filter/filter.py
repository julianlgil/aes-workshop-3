import json
from typing import Dict, List

from utils.utils import RabbitMQ
import time
import os


class Filter:
    def __init__(self, filter_keys: List[str] = None) -> None:
        self.filter_keys = filter_keys if filter_keys else os.getenv('FILTER_KEYS', '').split(',')

    def __find_key_in_list(self, key: str, items_list: List[str]):
        result = [item for item in items_list if key in item]
        return result != []

    def filter_by_genres(self, source: List[Dict]):
        ## noisy print(source)
        filter_result = {}
        for key in self.filter_keys:
            items_by_key = [{
                'name': item.get('name'),
                'popularity': item.get('popularity')
            } for item in source if self.__find_key_in_list(key=key, items_list=item.get('genres'))]
            filter_result.update({key: items_by_key})
        return filter_result


class RabbitCallback:
    def __init__(self, rabbit: RabbitMQ, queue_to_publish: str) -> None:
        self.queue_to_publish = queue_to_publish
        self.rabbit = rabbit

    def execute(self, ch, method, properties, body):
        try:
            source = body.decode('utf-8')
            filtered_message = Filter().filter_by_genres(source=json.loads(source))
            self.rabbit.publish(self.queue_to_publish, json.dumps(filtered_message))
            time.sleep(2)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error con el filtro: {e}")


if __name__ == '__main__':
    rabbit = RabbitMQ(amqp_url=os.environ['AMQP_URL'])
    source_queue = os.getenv('INITIAL_QUEUE_NAME')
    queue_to_publish = os.getenv('FILTER_QUEUE_NAME')
    rabbit.subscribe(source_queue, RabbitCallback(rabbit, queue_to_publish=queue_to_publish).execute)
