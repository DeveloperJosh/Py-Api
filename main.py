import flask
from flask import redirect, request, jsonify, render_template, session, url_for
from flask_session import Session
from data.nsfw import nsfw_image
import random
import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()
url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(url)
cur = conn.cursor()

app = flask.Flask(__name__, template_folder='html')
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "cookie"
Session(app)
image = []

def on_start():
    cur.execute("CREATE TABLE IF NOT EXISTS images (id serial PRIMARY KEY, image_url text, image_name text, image_nsfw boolean, image_tags text)")
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

@app.route(f'/api/v1/nsfw', methods=['GET'])
def api_v1_nsfw():
    json_data = { "Endpoints": ["/api/v1/nsfw/<id>", "/api/v1/nsfw/random"], "message": "Success" }
    return jsonify(json_data)

@app.errorhandler(404)
def page_not_found(e):
    error_data = { "message": "404 Page Not Found" }
    return jsonify(error_data), 404

@app.route(f'/api/v1/nsfw/<int:id>', methods=['GET'])
def api_v1_nsfw_id(id):
     if id > 4:
        return jsonify({"message": "Not found"})
     else:
        find_image = [nsfw_image[id-1]]
        for i in find_image:
            json_data = { "message": "Success", "url": i['url'] }
            return jsonify(json_data)

@app.route(f'/api/v1/nsfw/random', methods=['GET'])
def api_v1_nsfw_random():
        id = random.randint(1,4)
        find_image = [nsfw_image[id-1]]
        for i in find_image:
            json_data = { "message": "Success", "id": i['id'], "url": i['url'] }
            return jsonify(json_data)

@app.route(f'/api/v1/image/', methods=['GET'])
def api_v1_image():
    cur.execute("SELECT * FROM images")
    return jsonify(cur.fetchall())

@app.route(f'/api/v1/image/upload', methods=['POST', 'GET'])
def api_v1_image_post():
    if request.method == 'POST':
        request_data = request.get_json()
        image_url = request_data['url']
        number_generator = ''.join(random.choice('76378264862347632874632746') for i in range(4))
        cur.execute("INSERT INTO images (image_url, image_name, image_nsfw, image_tags) VALUES (%s, %s, %s, %s)", (image_url, number_generator, False, ""))
        conn.commit()
        return jsonify({"message": "Success"})
    elif request.method == 'GET':
        return jsonify({"message": "Please use POST"})

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
        ### get from request
        login = request.form
        email = login['email']
        password = login['password']
        if email == "":
            return jsonify({"message": "Please enter email"})
        elif password == "":
            return jsonify({"message": "Please enter password"})
        else:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            if user is None:
                return jsonify({"message": "User not found"})
            else:
                if password == user[1]:
                    ### add login session

                    session['logged_in'] = True
                    session['user_email'] = user[2]
                    return redirect(url_for('loggedin'))

                else:
                    return jsonify({"message": "Invalid Password"})
    if request.method == 'GET':
        return render_template('login.html')

@app.route(f'/loggedin', methods=['GET'])
def loggedin():
    if 'logged_in' in session:
        return jsonify({"message": "Success"})
    else:
        return jsonify({"message": "Error"})

@app.route(f'/register', methods=['POST'])
def register():
    if request.method == 'POST':
        ### get from request
        register = request.get_json()
        email = register['email']
        password = register['password']
        ### check if user exists
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        if user is None:
            cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
            conn.commit()
            return jsonify({"message": "Success"})
        else:
            return jsonify({"message": "User already exists"})

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