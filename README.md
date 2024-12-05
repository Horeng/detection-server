# OSS validation model driver

## How to run

```bash
./app.py
INFO 2024-12-05 22:05:55,842 - model config
INFO 2024-12-05 22:05:55,842 - name: file-example
request:
    type: file
        path: examples/detection-request.in
        value-type: json
report:
    type: file
    path: detection-report.out
    value-type: json

INFO 2024-12-05 22:05:55,843 - starting model runner thread
INFO 2024-12-05 22:05:55,843 - running with input from file examples/detection-request.in
INFO 2024-12-05 22:05:55,843 - will write report to file detection-report.out
...
```

## How to setup configuration file

- overview ([examples/example-conf.yml](examples/example-conf.yml))

```yaml
# detection system name
name: mockup
# input config (kafka, file)
request:
    type: kafka
    bootstrap-servers: ['192.168.49.2:30421']
    topic: dependency-graph
    value-type: json
# output config (kafka, file)
report:
    type: kafka
    bootstrap-servers: ['192.168.49.2:30421']
    topic: detection-result
    value-type: json
```

- request from a file ([examples/file-example.conf.yml](examples/file-example-conf.yml))

```yaml
request:
    type: file
    path: examples/detection-request.in
    value-type: json
```

- result to a file ([examples/file-example-conf.yml](examples/file-example-conf.yml))

```yaml
report:
    type: file
    path: detection-report.out
    value-type: json
```

## How to embed a model library to driver

modify `run_model` function in [model_runner.py](model_runner.py):

```python
def run_model(message):
    #time.sleep(5)
    logger.info(f"Processing message: {message}")
    # TODO report에 모델 실행 결과 저장
    report = 'call model library here and return result in string'
    return report 
```

## How to run a mockup API server

uncomment following line in [app.py](app.py):

```python
    #start_mock_api_server_thread(config)
```
