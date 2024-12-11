# OSS validation model driver

## 실행 방법

```bash
$ ./app.py -c {config file}
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

## 설정 파일

- yaml 형식으로 작성한다.
  - name: 모델 이름
  - request: 요청 입력 방식
  - report: 결과 출력 방식
- 예시: ([examples/example-conf.yml](examples/example-conf.yml))

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

- 요청을 파일에서 읽으려면 request 항목을 수정한다.
  - 예시: ([examples/file-example.conf.yml](examples/file-example-conf.yml))

```yaml
request:
    type: file
    path: examples/detection-request.in
    value-type: json
```

- 결과를 파일로 쓰려면 report 항목을 수정한다.
  - 예시: ([examples/file-example-conf.yml](examples/file-example-conf.yml))

```yaml
report:
    type: file
    path: detection-report.out
    value-type: json
```

## 모델 코드 연동

- [model_runner.py](model_runner.py) 파일의 run_model 함수에서 모델 실행 함수를 호출한다.
  - [mockup](mock/model_mock.py) 호출 예제를 참고

```python
def run_model(message):
    #time.sleep(5)
    logger.info(f"Processing message: {message}")
    # TODO report에 모델 실행 결과 저장
    report = 'call model library here and return result in string'
    return report 
```

## 요청 입력을 kafka로 받을 경우 테스트용 mockup API 서버 실행 방법

- 실행 인자에 -m(--mock) 옵션을 지정한다.

