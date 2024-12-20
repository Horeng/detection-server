# Imports - Standard
import json

# Imports - Third-party
from kafka import KafkaProducer


value_serializers = {
    'json': lambda x: json.dumps(x).encode('utf-8'),
}


class KafkaProducerConfig:
    def __init__(self, bootstrap_servers, value_type):
        self.bootstrap_servers = bootstrap_servers
        self.value_serializer = value_serializers[value_type]


def get_producer(config):
    return KafkaProducer(
        bootstrap_servers=config.bootstrap_servers,
        value_serializer=config.value_serializer
    )


def produce(producer, topic, key, value):
    producer.send(
        topic,
        key=key.encode('utf-8') if key else None,
        value=value.replace('\n', ' ')
    )
