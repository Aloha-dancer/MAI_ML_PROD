from flask import Flask, json, request, jsonify
import requests
from dotenv.main import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/', methods = ['PUT', 'POST'])
def redirect():
    data = request.get_json()

    response = requests.get(f'http://{os.environ["ML_HOST"]}:{os.environ["ML_PORT"]}/predict', json = data)


    if response.status_code == '200':
        if requests.get('http://192.168.96.3:/check', ):
            requests.post('localhost:5000/')

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'Service': 'EmailHandler', 'Status': '200'})

if __name__ == "__main__":
    app.run(host = '0.0.0.0',
            port = 3000)