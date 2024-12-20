# Imports - Standard
import unittest

# Imports - Local
from config import Config, ConfigError, read_config


class ConfigTest(unittest.TestCase):

    def test_file_config_example(self):
        config_file = 'file-example-conf.yml'
        config = read_config(config_file)
        self.assertEqual(config.request_type, 'file')
        self.assertEqual(config.request_file_path, 'detection-request.in')
        self.assertEqual(config.request_value_type, 'json')
        self.assertEqual(config.report_type, 'file')
        self.assertEqual(config.report_file_path, 'detection-report.out')
        self.assertEqual(config.report_value_type, 'json')

    def test_kafka_config_example(self):
        config_file = 'kafka-example-conf.yml'
        config = read_config(config_file)
        self.assertEqual(config.request_type, 'kafka')
        self.assertEqual(len(config.request_bootstrap_servers), 1)
        self.assertEqual(config.request_topic, 'request-topic')
        self.assertEqual(config.request_value_type, 'json')
        self.assertEqual(len(config.report_bootstrap_servers), 2)
        self.assertEqual(config.report_topic, 'report-topic')
        self.assertEqual(config.report_value_type, 'json')


if __name__ == '__main__':
    unittest.main()

