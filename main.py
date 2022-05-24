import flask
from flask import request, jsonify
from data.nsfw import nsfw_image
import random
import json
import string

app = flask.Flask(__name__)
app.config["DEBUG"] = True

with open('data/config.json', 'r') as json_file:
    config = json.load(json_file)
    token = config['token']

@app.route('/api/v1/getkey', methods=['GET'])
def get_token():
    return jsonify({'message': 'You need to join the server for the key'})

@app.route('/', methods=['GET'])
def home():
    headers = request.headers
    auth = headers.get('Authorization')
    if auth == token:
        return jsonify({'message': 'Welcome to the NSFW API'})
    else:
        return jsonify({'message': 'You need to join the server for the key'})


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