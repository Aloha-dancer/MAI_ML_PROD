from flask import Flask, render_template, json, request, jsonify
import psycopg2
from dotenv.main import load_dotenv
import os
import requests

load_dotenv()
host = os.environ['PG_HOST']
port = os.environ['PG_PORT']
database = os.environ['PG_DB_NAME']
user = os.environ['PG_DB_USER']
pwd = os.environ['PG_PASSWORD']
app = Flask(__name__)

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
                       INSERT INTO user (first_name, email, login, password, last_name)
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

@app.route('/addmsg', methods = ['POST'])
def add_message():
    json_content = request.get_json()

    response = requests.get(f'http://{os.environ["ML_HOST"]}:{os.environ["ML_PORT"]}/test', json = json_content)
    status_code = response.status_code
    json_content = response.json()
    if response.status_code == '200':

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
                """
                    INSERT INTO public.message (date, user_id, text, label)
                    VALUES (now(), 1, 'asfasf', 'label')
                """
               )

        conn.commit()
        conn.close()
        js = response.json()
    
    return json.dumps({'Status': f"{status_code}", "Content": f"{json_content}"}) if status_code else "{'1': '1'}"

@app.route('/test', methods = ['GET'])
def test():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT 'Service', 'Postgres', 'Status', '200'")
    conn.commit()

    status_row = cur.fetchone()

    conn.close()

    response_ml = requests.get(f'http://{os.environ["ML_HOST"]}:{os.environ["ML_PORT"]}/test')
    response_email = requests.get(f'http://{os.environ["EMAIL_HOST"]}:{os.environ["EMAIL_PORT"]}/test')

    finale_json = jsonify({'ML': f'{response_ml.json()}',
                           'Email': f'{response_email.json()}',
                           'DB': "{%s: %s}, {%s: %s}" % (status_row[0], 
                                                         status_row[1],
                                                         status_row[2],
                                                         status_row[3])
                           })
if __name__ == "__main__":
    app.run(host = '0.0.0.0',
            port = 5000)