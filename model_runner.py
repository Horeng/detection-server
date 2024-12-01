from functools import partial
import logging
import time

from kafka_utils import kafka_pub, kafka_sub


logger = logging.getLogger(__name__)
task_status = 'WAITING'


# kafka에서 메시지를 읽어서 처리하고 결과를 반환하는 작업 반복
def run_and_report(config):
    bootstrap_servers = config['kafka']['bootstrap-servers']
    request_topic = config['kafka']['request']['topic']
    request_value_type = config['kafka']['request']['value-type']
    report_topic = config['kafka']['report']['topic']
    report_value_type = config['kafka']['report']['value-type']
    key = config['model']['name']

    producer_config = kafka_pub.KafkaProducerConfig(
        bootstrap_servers=bootstrap_servers,
        value_type=report_value_type
    )
    producer = kafka_pub.get_producer(producer_config)

    consumer_config = kafka_sub.KafkaConsumerConfig(
        bootstrap_servers=bootstrap_servers,
        topic=request_topic,
        auto_offset_reset='latest',
        group_id='detection-server-1',
        value_type=request_value_type
    )
    consumer = kafka_sub.get_consumer(consumer_config)

    for message in consumer:
        global task_status
        task_status = 'RUNNING'
        # 탐지 모델을 수행한 다음 결과를 kafka로 전송
        report = run_model(message.value, producer)
        # TODO report status에 따른 처리
        kafka_pub.produce(producer, report_topic, key, report)
        task_status = 'WAITING'
        consumer.commit()


# 모델 실행 후 결과 반환
def run_model(message, producer):
    #time.sleep(5)
    logger.info(f"Processing message: {message}")
    # TODO report에 모델 실행 결과 저장
    report = 'result'
    return report 


def get_status():
    return task_status

