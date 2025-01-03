# Imports - Standard
from functools import partial
import json
import logging

# Imports - Third-party
from kafka_utils import kafka_pub, kafka_sub

# Imports - Local
from mocks import model_mock


logger = logging.getLogger(__name__)
task_status = 'WAITING'


def get_report_func(config):
    if config.report_type.lower() == 'file':
        logger.info(f'will write report to file {config.report_file_path}')
        output_file = open(config.report_file_path, 'w')
        return lambda report: \
            output_file.writelines([ report + '\n' ])
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


# 파일 내용으로 모델을 실행하고 결과를 반환
def run_loop_file_input(config):
    report_func = get_report_func(config)

    with open(config.request_file_path, 'r') as input_file:
        for message in input_file:
            global task_status
            task_status = 'RUNNING'
            try:
                # 모델 실행 함수
                report = run_model(json.loads(message))
                # TODO report status에 따른 처리
                logger.info(f'report: {report}')
                report_func(report)
            except Exception as e:
                logger.warn(f'exception occurred while model runs: {e}')
            task_status = 'WAITING'


# kafka 메시지로 모델을 실행하고 결과를 반환
def run_loop_kafka_input(config):
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
        try:
            consumer.commit()
            # 모델 실행 함수
            report = run_model(message.value)
            logger.info(f'report: {report}')
            # TODO report status에 따른 처리
            report_func(report)
        except Exception as e:
            logger.warn(f'exception occurred while model runs: {e}')
        task_status = 'WAITING'


def run(config):
    if config.request_type.lower() == 'file':
        logger.info(f'running with input from file {config.request_file_path}')
        run_loop_file_input(config)
    else:    # config.request_type.lower() == 'kafka'
        logger.info(f'running with input from kafka topic {config.request_topic}')
        run_loop_kafka_input(config)


# 모델 실행 후 결과 반환
# request_message는 json string이 아니라 dict object여야 함
def run_model(request_message):
    logger.info(f"Processing message: {request_message}")
    # TODO report에 모델 실행 결과 저장
    report = model_mock.run_model(request_message)
    return report 


def get_status():
    global task_status
    return task_status

