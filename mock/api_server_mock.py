import time

from kafka_utils import kafka_pub


def run_mock_api_server(config):
    bootstrap_servers = config['kafka']['bootstrap-servers']
    request_topic = config['kafka']['request']['topic']
    value_type = config['kafka']['request']['value-type']
    key = config['model']['name']
    dummy_request = '''
    {
        "packageList": "package-list",
        "packageMetadata": "package-metadata"
    }
    '''

    producer_config = kafka_pub.KafkaProducerConfig(
        bootstrap_servers=bootstrap_servers,
        value_type=value_type
    )
    producer = kafka_pub.get_producer(producer_config)

    while True:
        kafka_pub.produce(producer, request_topic, key, dummy_request)
        time.sleep(10)
