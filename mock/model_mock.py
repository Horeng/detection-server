import json
import time


def run_model(request_message):
    token = request_message['token']
    report_template = '''
    {
        "modelName": "mock",
        "token": "%s",
        "report": "report"
    }
    '''
    time.sleep(3)
    return report_template % token
