from flask import Flask, render_template, request, jsonify
import json
import psycopg2
from dotenv.main import load_dotenv
import os
import requests

import subprocess as s

app = Flask(__name__)

load_dotenv()
host = os.environ['PG_HOST']
port = os.environ['PG_PORT']
database = os.environ['PG_DB_NAME']
user = os.environ['PG_DB_USER']
pwd = os.environ['PG_PASSWORD']


def get_db_connection():
    conn = psycopg2.connect(host = host,
                            database = database,
                            user = user,
                            port = port,
                            password = pwd)
    return conn

'''
Static content
'''

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignIn')
def showSignIn():
    render_template('signin.html')

'''
Requests for server
'''

@app.route('/signUp', methods = ['POST'])
def signUp():
    # read the posted values from the UI 
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _login = request.form['inputLogin']
    _password = request.form['inputPassword']
    _last_name = request.form['inputLastName']

    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
                   SELECT 1 
                   FROM user
                   WHERE EXISTS(
                                SELECT 1
                                FROM user
                                WHERE ' email' = '%s' OR
                                      ' login' = '%s'      
                         )
                """ % (_email, _login)
               )
    conn.commit()
    if cur.fetchone():
        return json.dumps({'user': f'{_login} already exists!'})
    else:

        import hashlib

        salt = os.urandom(32)

        _hashed_pwd = hashlib.pbkdf2_hmac(
                                          'sha256',
                                          _password.encode('utf-8'),
                                          salt,
                                          100000,
                                          dklen = 128
                                         )
        cur.execute("""
                       INSERT INTO public.user (first_name, email, login, password, last_name)
                       VALUES (%s, %s, %s, %s, %s)
                    """ % (_name, _email, _login, salt + _hashed_pwd, _last_name))
        conn.commit()
        conn.close()

        return json.dumps({'Response': f'User {_login} sucessfully created!'})

@app.route('/signIn', methods = ['POST'])
def singIn():
    #read the posted valeus from the UI
    _user = request.form['inputUser']
    _password = request.form['inputPassword']

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
                """
                   SELECT 1 
                   FROM user 
                   WHERE EXISTS(
                                 SELECT user_id
                                 FROM user
                                 WHERE ' email' = '%s' OR 
                                       ' login' = '%s'
                         )
                 """ % (_user, _user)
               )


def add_message(data):
    json_content = data

    if len(json_content):
        conn = get_db_connection()
        cur = conn.cursor()
        pred = 'spam' if int(json_content['Predicted_label']) else 'ham'
        cur.execute(
                """
                    INSERT INTO public.message (date, user_id, subject, content, text, label)
                    VALUES (now(), 3, '%s', '%s', '%s', '%s')
                """ % (json_content['Content'][0], 
                       json_content['Content'][1],
                       json_content['Content'][2],
                       pred)
               )

        conn.commit()
        conn.close()

@app.route('/getcontent', methods = ['GET'])
def get_content():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
                """
                    SELECT email,
                           content,
                           subject,
                           label
                    FROM public.message msg
                    JOIN public.user u ON
                    msg.user_id = u.user_id
                """
                )
    
    conn.commit()
    
    data_js = []
    for i in cur.fetchall():
        data_js.append({'user_id': i[0],
                        'message': i[1],
                        'subject': i[2],
                        'label': i[3]})
    conn.close()
    return json.dumps(data_js)

@app.route('/predict', methods = ['POST'])
def get_prediction():
    data = request.get_json()
    
    response = requests.get(f'http://{os.environ["ML_HOST"]}:{os.environ["ML_PORT"]}/predict', params = json.loads(data))
    if response.status_code == 200:
        predicted_values = response.json()
        add_message(predicted_values)
        return json.dumps(response.json())
    
    return json.dumps({'1':'1'})

@app.route('/test', methods = ['GET'])
def test():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT 'Service', 'Postgres', 'Status', '200'")
    conn.commit()

    status_row = cur.fetchone()

    conn.close()
    response_ml = requests.get(f'http://{os.environ["ML_HOST"]}:{os.environ["ML_PORT"]}/test')
    try:
        response_email = requests.get(f'http://{os.environ["EMAIL_HOST_1"]}:{os.environ["EMAIL_PORT"]}/test')
    except requests.exceptions.ConnectionError:
        response_email = requests.get(f'http://{os.environ["EMAIL_HOST_2"]}:{os.environ["EMAIL_PORT"]}/test')

    finale_json = jsonify({'ML': f'{response_ml.json()}',
                           'Email': f'{response_email.json()}',
                           'DB': "{%s: %s}, {%s: %s}" % (status_row[0], 
                                                         status_row[1],
                                                         status_row[2],
                                                         status_row[3])
                           })
    return finale_json
if __name__ == "__main__":
    app.run(host = '0.0.0.0',
            port = 5000)