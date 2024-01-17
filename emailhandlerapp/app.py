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
    js = json.dumps(data, allow_nan = True, indent = 4)
    response = requests.get(f'http://{os.environ["ML_HOST"]}:{os.environ["ML_PORT"]}/predict', json = js)
    return response.json()
    return response.json()

    if response.status_code == '200':
        post_response = requests.post(f'http://{os.environ["MAIN_HOST"]}:{os.environ["MAIN_PORT"]}/addmsg', json = predicted_data)
        return jsonify({'Response': 'Sucess'})
    else:
        return jsonify({'Request_error': f'{response.status_code}'})
    

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'Service': 'EmailHandler', 'Status': '200'})

if __name__ == "__main__":
    app.run(host = '0.0.0.0',
            port = 3000)