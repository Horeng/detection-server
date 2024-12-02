#!/usr/bin/python3

from flask import Flask, jsonify
from functools import partial
import logging
import sys
import threading
import yaml

import model_runner
from conf.config import read_config
from mock import api_server_mock


app = Flask(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(levelname)s %(asctime)s - %(message)s'
)
logger = logging.getLogger(__name__)


# 모델 실행 상태 반환
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(model_runner.get_status())


# 모델 실행 스레드
def start_model_runner_thread(config):
    logger.info('starting model runner thread')
    consumer_thread = threading.Thread( \
        target=partial(model_runner.run_and_report, config))
    consumer_thread.daemon = True
    consumer_thread.start()


# 테스트용 api 서버 실행 스레드
def start_mock_api_server_thread(config):
    logger.info('starting mock api server thread')
    mock_server_thread = threading.Thread( \
        target=partial(api_server_mock.run_mock_api_server, config))
    mock_server_thread.daemon = True
    mock_server_thread.start()


if __name__ == '__main__':
    config = read_config('conf/example-conf.yml')

    # 모델 실행 스레드 시작
    start_model_runner_thread(config)
    #start_mock_api_server_thread(config)

    # Flask 서버 실행
    app.run(host='0.0.0.0', port=5000)

