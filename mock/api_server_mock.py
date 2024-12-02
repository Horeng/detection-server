import time

from kafka_utils import kafka_pub


def run_mock_api_server(config):
    key = config.name
    dummy_request = '''
    {
        "packageList": "package-list",
        "packageMetadata": "package-metadata"
    }
    '''

    producer_config = kafka_pub.KafkaProducerConfig(
        bootstrap_servers=config.report_bootstrap_servers,
        value_type=config.report_value_type
    )
    producer = kafka_pub.get_producer(producer_config)

    while True:
        kafka_pub.produce(producer, config.request_topic, key, dummy_request)
        time.sleep(10)
