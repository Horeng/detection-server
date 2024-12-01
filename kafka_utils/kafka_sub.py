from kafka import KafkaConsumer
import json


value_deserializers = {
    'json': lambda x: json.loads(x.decode('utf-8')),
}


class KafkaConsumerConfig:
    def __init__(self, bootstrap_servers, topic, auto_offset_reset, group_id, value_type):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.auto_offset_reset = auto_offset_reset
        self.group_id = group_id
        self.value_deserializer = value_deserializers[value_type]


def get_consumer(config):
    return KafkaConsumer(
        config.topic,
        bootstrap_servers=config.bootstrap_servers,
        auto_offset_reset=config.auto_offset_reset,
        enable_auto_commit=True,
        group_id=config.group_id,
        value_deserializer=config.value_deserializer
    )
