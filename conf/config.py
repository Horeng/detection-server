import logging
import yaml


logger = logging.getLogger(__name__)


class ConfigError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Config:

    def __init__(self, yaml_config, yaml_path):
        try:
            self.name = yaml_config['name']
            self.read_request_config(yaml_config['request'])
            self.read_report_config(yaml_config['report'])
        except KeyError as e:
            logger.error(f'required key does not exist in config file {yaml_path}')
            raise e

    def read_request_config(self, yaml):
        self.request_type = yaml['type']
        if self.request_type.lower() == 'kafka':
            self.request_bootstrap_servers = yaml['bootstrap-servers']
            self.request_topic = yaml['topic']
        elif self.request_type.lower() == 'file':
            self.request_file_path = yaml['path']
        else:
            raise ConfigError(f'invalid request type {self.request_type}')
        self.request_value_type = yaml['value-type']

    def read_report_config(self, yaml):
        self.report_type = yaml['type']
        if self.report_type.lower() == 'kafka':
            self.report_bootstrap_servers = yaml['bootstrap-servers']
            self.report_topic = yaml['topic']
        elif self.report_type.lower() == 'file':
            self.report_file_path = yaml['path']
        else:
            raise ConfigError(f'invalid report type {self.report_type}')
        self.report_value_type = yaml['value-type']


# 설정 파일 읽기
def read_config(config_file):
    with open(config_file) as config_stream:
        logger.info('model config')
        logger.info(config_stream.read())
        try:
            config_stream.seek(0)
            config = Config(yaml.safe_load(config_stream), config_file)
            return config
        except yaml.YAMLError as e:
            logger.error(e)
            raise e

