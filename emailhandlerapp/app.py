from flask import Flask, request, jsonify
import json
import requests
from dotenv.main import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/', methods = ['PUT', 'POST'])
def redirect():
    data = request.get_json()
    
    response = requests.post(f'http://{os.environ["MAIN_HOST"]}:{os.environ["MAIN_PORT"]}/predict', json = data)
    return json.dumps(response.json())

    

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'Service': 'EmailHandler', 'Status': '200'})

if __name__ == "__main__":
    app.run(host = '0.0.0.0',
            port = 3000)