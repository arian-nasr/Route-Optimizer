from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

# configuration
DEBUG = True

# api keys
apiKey = os.environ.get('MAPS_API_KEY')

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/route', methods=['GET'])
def route():
    origin = request.args.get('org')
    destination = request.args.get('dest')
    waypoints = request.args.get('way')
    query = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&waypoints=optimize:true{}&key={}".format(origin, destination, waypoints, apiKey)
    r = requests.get(url = query)
    data = r.json()
    return data

if __name__ == '__main__':
    app.run(host="192.168.0.21")
