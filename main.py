import flask
from flask import request, jsonify
from data.nsfw import nsfw_image
import random
import json
import string

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY']='9nwof9uwfqoko99'

@app.route('/api/v1/getkey', methods=['GET'])
def get_token():
    with open('data/config.json', 'w') as f:
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        ip_addr = request.remote_addr
        f.write(json.dumps({'ip_addr': ip_addr, 'token': token}))
        f.close()
    return jsonify({'token': token})

with open('data/config.json', 'r') as f:
    config = json.load(f)
    token = config['token']

@app.route('/client')
def client():
    ip_addr = request.environ['REMOTE_ADDR']
    return '<h1> Your IP address is:' + ip_addr

@app.route('/', methods=['GET'])
def home():
    header = request.headers.get('Authorization')
    if header == token:
        return jsonify({'message': "Authorized"})
    else:
        return jsonify({'message': "Unauthorized"})


@app.route(f'/api/v1/', methods=['GET'])
def api_v1():
    json_data = { "message": "No Endpoins Used" }
    return jsonify(json_data)

@app.route(f'/api/v1/nsfw/', methods=['GET'])
def api_v1_nsfw():
    headers = request.headers
    auth = headers.get("Authorization")
    if auth == token:
        json_data = { "Endpoints": ["/api/v1/nsfw/<id>", "/api/v1/nsfw/random"], "message": "Success" }
        return jsonify(json_data)
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route(f'/api/v1/nsfw/<int:id>', methods=['GET'])
def api_v1_nsfw_id(id):
    headers = request.headers
    auth = headers.get("Authorization")
    if auth == token:
     if id > 3:
        return jsonify({"message": "Not found"})
     else:
        find_image = [nsfw_image[id-1]]
        for i in find_image:
            json_data = { "message": "Success", "url": i['url'] }
            return jsonify(json_data)
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401

@app.route(f'/api/v1/nsfw/random', methods=['GET'])
def api_v1_nsfw_random():
    headers = request.headers
    auth = headers.get("Authorization")
    if auth == token:
        id = random.randint(1,3)
        find_image = [nsfw_image[id-1]]
        for i in find_image:
            json_data = { "message": "Success", "id": i['id'], "url": i['url'] }
            return jsonify(json_data)
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401