from concurrent.futures import process
from tabnanny import check
import flask
from flask import request, jsonify
from data.nsfw import nsfw_image
import random
import json
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = True

image = []

def get_random_image():
    ###check for new images
    try:
        with open('data/images.json', 'r') as f:
            image = json.load(f)
    except:
        return jsonify({"error": "No images found"})
    while True:
        random_index = random.randint(0, len(image)-1)
        print("Random index:", random_index)
        if len(image) == 0:
            return jsonify({"error": "No images found."})
        else:
            return image[random_index]

def auto_dump():
    with open('data/images.json', 'w') as f:
        json.dump(image, f)
    print("Dumping...")

def auto_clear():
    with open('data/images.json', 'w') as f:
        json.dump([], f)
    print("Clearing...")

@app.route('/', methods=['GET'])
def home():
      return jsonify({'message': 'Welcome to Blue\'s API'})

@app.route(f'/api/v1/', methods=['GET'])
def api_v1():
    json_data = { "message": "No Endpoins Used" }
    return jsonify(json_data)

@app.route(f'/api/v1/nsfw/', methods=['GET'])
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
    return jsonify(get_random_image())

@app.route(f'/api/v1/image/upload', methods=['POST', 'GET'])
def api_v1_image_post():
    if request.method == 'POST':
        request_data = request.get_json()
        image_url = request_data['url']
        number_generator = ''.join(random.choice('76378264862347632874632746') for i in range(4))
        image_data = {'id': number_generator, 'url': image_url}
        image.append(image_data)
        auto_dump()
        return jsonify({"message": "Success"})
    elif request.method == 'GET':
        return jsonify({"message": "Please use POST"})

@app.route(f'/dev/clear', methods=['GET'])
def dev_clear():
    headers = request.headers
    auth = headers.get("Authorization")
    if auth == os.environ.get("DEV_AUTH"):
        auto_clear()
        return jsonify({"message": "Success"})
    else:
        return jsonify({"message": "Invalid Authorization"})