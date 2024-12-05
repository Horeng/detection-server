from functools import partial
import logging
import time

from kafka_utils import kafka_pub, kafka_sub


logger = logging.getLogger(__name__)
task_status = 'WAITING'


def get_report_func(config):
    if config.report_type.lower() == 'file':
        logger.info(f'will write report to file {config.report_file_path}')
        output_file = open(config.report_file_path, 'w')
        return lambda report: \
            output_file.writelines([ report + '\n' ])
            #print('report: ' + report) \

    else:    # config.report_type.lower() == 'kafka':
        logger.info(f'will write report to kafka topic {config.report_topic}')
        producer_config = kafka_pub.KafkaProducerConfig(
            bootstrap_servers=config.report_bootstrap_servers,
            value_type=config.report_value_type
        )
        producer = kafka_pub.get_producer(producer_config)
        key = config.name
        return lambda report: \
            kafka_pub.produce(producer, config.report_topic, key, report)


def run_with_file_input(config):
    report_func = get_report_func(config)

    with open(config.request_file_path, 'r') as input_file:
        for message in input_file:
            global task_status
            task_status = 'RUNNING'
            report = run_model(message)
            # TODO report status에 따른 처리
            report_func(report)
            task_status = 'WAITING'


def run_with_kafka_input(config):
    consumer_config = kafka_sub.KafkaConsumerConfig(
        bootstrap_servers=config.request_bootstrap_servers,
        topic=config.request_topic,
        auto_offset_reset='latest',
        group_id='detection-server-1',
        value_type=config.request_value_type
    )
    consumer = kafka_sub.get_consumer(consumer_config)

    report_func = get_report_func(config)

    for message in consumer:
        global task_status
        task_status = 'RUNNING'
        # 탐지 모델을 수행한 다음 결과를 kafka로 전송
        report = run_model(message.value)
        # TODO report status에 따른 처리
        report_func(report)
        task_status = 'WAITING'
        consumer.commit()


# kafka에서 메시지를 읽어서 처리하고 결과를 반환하는 작업 반복
def run_and_report(config):
    if config.request_type.lower() == 'file':
        logger.info(f'running with input from file {config.request_file_path}')
        run_with_file_input(config)
    else:    # config.request_type.lower() == 'kafka'
        logger.info(f'running with input from kafka topic {config.request_topic}')
        run_with_kafka_input(config)


# 모델 실행 후 결과 반환
def run_model(message):
    #time.sleep(5)
    logger.info(f"Processing message: {message}")
    # TODO report에 모델 실행 결과 저장
    report = '{ "detection result": "success" }'
    return report 


def get_status():
    return task_status

