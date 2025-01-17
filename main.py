# Imports - Standard
from functools import partial
import argparse
import logging
import sys
import threading

# Imports - Third-party

# Imports - Local
import model_runner
from conf.config import read_config
from mocks import api_server_mock


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(levelname)s %(asctime)s - %(message)s'
)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    prog='app.py'
)
parser.add_argument('-c', '--conf', required=True, help='config file (required)')
parser.add_argument('-m', '--mock', action='store_true', help='run input(api server) mockup along')


# 모델 실행 스레드
def start_model_runner_thread(config):
    logger.info('starting model runner thread')
    consumer_thread = threading.Thread(target=partial(model_runner.run, config))
    consumer_thread.daemon = True
    consumer_thread.start()


# 테스트용 api 서버 실행 스레드
def start_mock_api_server_thread(config):
    logger.info('starting mock api server thread')
    mock_server_thread = threading.Thread( \
        target=partial(api_server_mock.run_mock_api_server, config))
    mock_server_thread.daemon = True
    mock_server_thread.start()


def server_main():
    args = parser.parse_args()

    # 설정 파일 읽기
    config = read_config(args.conf)

    # 모델 실행 스레드 시작
    start_model_runner_thread(config)

    # API 서버 mockup 시작
    if args.mock:
        start_mock_api_server_thread(config)

