#!/usr/bin/python3

# Imports - Standard
import os
from flask import Flask, jsonify

# Imports - Local
from main import server_main
import model_runner


app = Flask(__name__)


# 모델 실행 상태 반환
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(model_runner.get_status())


if __name__ == '__main__':
    server_main()

    # Flask 서버 실행
    app.run(host=os.getenv('FLASK_HOST', '0.0.0.0'),
            port=os.getenv('FLASK_PORT', 5000))

