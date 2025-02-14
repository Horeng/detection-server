# OSS validation model driver

## 설치 방법

- 파이썬 버전 3.11
- 파이썬 패키지 관리 도구 [uv](https://docs.astral.sh/uv/)
  - uv 설치 방법은 [uv 공식 문서](https://github.com/astral-sh/uv?tab=readme-ov-file#installation)를 참고한다.
```bash
$ cd some_where/detection-server
```

#### 방법#1 - uv 사용 시

```bash
$ uv venv
$ source .venv/bin/activate
$ uv sync

# 새로운 패키지를 설치할 경우
$ uv add {package}
```


#### 방법#2 - pip 사용 시

```bash
$ pip install flask kafka-python PyYAML

# requirements.txt 파일을 사용할 경우
$ pip install -r requirements.txt
```

## 실행 방법

```bash
$ ./app.py -h
usage: app.py [-h] -c CONF [-m]

options:
  -h, --help            show this help message and exit
  -c CONF, --conf CONF  config file (required)
  -m, --mock            run mock api server along
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

- 입출력을 kafka 대신 파일로 읽고 쓰도록 설정할 수 있다.
```yaml
# request만 바꿔도 된다.
request:
    type: file
    path: examples/detection-request.in
    value-type: json

# report만 바꿔도 된다.
report:
    type: file
    path: detection-report.out
    value-type: json
```

## 모델 코드 연동

- [model_runner.py](model_runner.py) 파일의 run_model 함수에서 모델 실행 함수를 호출한다.
```python
def run_model(model_name, request_message):
    ...
    # 입력 인자(request_data)를 모델 실행 인자로 전달하고 report에 모델 실행 결과 저장
    # 이 코드 라인에서 호출하는 'model_func'가 실제 모델 함수로 바꿔야 한다.
    model_result = model_func(request_data)
    ...
```

- 모델 실행 함수는 탐지 결과를 문자열 형식으로 반환하면 된다. (형식은 필요없다)
- 서버 함수가 아래와 같은 형식으로 kafka에 응답하거나 파일에 기록한다.
```json
{
  "token": "(요청으로 받은 토큰)",
  "modelName": "(설정 파일에 지정한 모델 이름)",
  "report": "(탐지 모델이 생성한 결과)"
}
```

## API 서버 테스트

- [TestAPIServerWithKafka.ipynb](examples/TestAPIServerWithKafka.ipynb) 파일을 참고한다.
