from distutils.log import error
import flask
from flask import make_response, redirect, request, jsonify, render_template, session, url_for
import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()
url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(url)
cur = conn.cursor()

app = flask.Flask(__name__, template_folder='html')
app.config['SECRET_KEY'] = 'UIHFIUGIEGAKRFEWUYDGYDGFIUYAEWGUYFEGWYUGAEiFUAGEUYFGIUEATGFUYEGWUYFAGYEATUYFET6T6783647823YDEFQGUYASDGUYDTQW7863875631278t67'
app.config["DEBUG"] = True

def on_start():
    ### users table
    cur.execute("CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, password text, email text)")
    conn.commit()

on_start()

@app.route('/', methods=['GET'])
def home():
      return render_template('index.html')

@app.route(f'/api/v1', methods=['GET'])
def api_v1():
    json_data = { "message": "No Endpoins Used" }
    return jsonify(json_data)

@app.errorhandler(404)
def page_not_found(e):
    error_data = { "message": "404 Page Not Found" }
    return jsonify(error_data), 404

@app.route(f'/dev/clear', methods=['GET'])
def dev_clear():
    headers = request.headers
    auth = headers.get("Authorization")
    if auth == os.environ.get("DEV_AUTH"):
        cur.execute("DELETE FROM *")
        conn.commit()
        return jsonify({"message": "Success"})
    else:
        return jsonify({"message": "Invalid Authorization"})

@app.route(f'/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login = request.form
        email = login['email']
        password = login['password']
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        if user is None:
            return jsonify({"message": "User Not Found"}), 200
        else:
            if password == user[1]:
                session['email'] = user[0]
                return redirect(url_for('userpage'))
            else:
                return jsonify({"message": "Invalid Password"})

    if request.method == 'GET':
        return render_template('login.html')

@app.route(f'/logout', methods=['GET'])
def logout():
    resp = make_response(redirect(url_for('home')))
    session.pop('email', None)
    resp.set_cookie('email', '', expires=0)
    return resp


@app.route(f'/userpage', methods=['GET'])
def userpage():
    ### check if user email in cookies
    if 'email' in session:
        email = session['email']
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        return render_template('userpage.html', user = user)
    else:
        return redirect(url_for('login'))

@app.route(f'/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        ### get from request
        register = request.form
        email = register['email']
        password = register['password']
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        if user is None:
            cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
            conn.commit()
            return redirect(url_for('login'))
        else:
            return jsonify({"message": "User already exists"})
    if request.method == 'GET':
        return render_template('register.html')

@app.route(f'/delete/user', methods=['DELETE'])
def delete_users():
    if request.method == 'DELETE':
        email = request.args.get("email")
        headers = request.headers
        auth = headers.get("Authorization")
        if auth == os.environ.get("DEV_AUTH"):
            cur.execute("DELETE FROM users WHERE email = %s", (email,))
            conn.commit()
            return jsonify({"message": "Success"})
        else:
            return jsonify({"message": "Invalid Authorization"})

@app.route(f'/delete/account', methods=['GET'])
def delete_account():
    if request.method == 'GET':
        email = request.cookies.get("email")
        if email is None:
            print("No email in cookies")
            return redirect(url_for('userpage'))
        else:
            cur.execute("DELETE FROM users WHERE email = %s", (email,))
            conn.commit()
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('email', '', expires=0)
            return resp
