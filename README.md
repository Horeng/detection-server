# OSS validation model driver

## 실행 방법

```bash
$ ./app.py -c {config file}
```

## 설정 파일

- yaml 형식으로 작성한다.
  - name: 모델 이름
  - request: 요청 입력 방식
  - report: 결과 출력 방식
```yaml
# detection system name
name: my-system
# input config (kafka, file)
request:
    type: kafka
    bootstrap-servers: ['host:port']
    topic: request
    value-type: json
# output config (kafka, file)
report:
    type: kafka
    bootstrap-servers: ['host:port']
    topic: result
    value-type: json
```

- 요청을 파일에서 읽으려면 request 항목을 수정한다.
```yaml
request:
    type: file
    path: examples/detection-request.in
    value-type: json
```

- 실행 결과를 파일로 쓰려면 report 항목을 수정한다.
```yaml
report:
    type: file
    path: detection-report.out
    value-type: json
```

## 모델 코드 연동

- [model_runner.py](model_runner.py) 파일의 run_model 함수에서 모델 실행 함수를 호출한다.
```python
def run_model(message):
    ...
    # 입력 인자(message)를 모델 실행 인자로 전달하고 report에 모델 실행 결과 저장
    report = model_func(message)
    return report
```

## 요청 입력을 kafka로 받을 경우 테스트용 mockup API 서버 실행 방법

- 실행 인자에 -m(--mock) 옵션을 지정한다.
```bash
$ ./app.py -c {config file} -m
```

