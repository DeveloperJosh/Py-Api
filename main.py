import flask
from flask import request, jsonify
import json
import random

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    ### json response
    json_data = { "message": "Hello World!" }
    
    return jsonify(json_data)

@app.route('/api/v1', methods=['GET'])
def api_v1():
    ### json response
    json_data = { "message": "Api Is not open" }
    
    return jsonify(json_data)

@app.route('/api/v1/porn', methods=['GET'])
def api_v1_port():
    nsfw_image = [
    {'id': 1,
    'url': 'https://himg.nl/images/sex/228f79894afc73a218416e20ae74fd17/original.gif',
    },
    {'id': 2,
    'url': 'https://myteenwebcam.com/fapp/gifs/007afbdbfc1da0ea5cb00b19eff93306.gif',
     },
    {'id': 3,
    'url': 'https://cdn.porngifs.com/img/16894',
    },

   ]
    id = random.randint(1,3)
    find_image = [nsfw_image[id-1]]
    return jsonify(find_image)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()