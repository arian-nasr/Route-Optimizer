from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import os

# configuration
DEBUG = True

# api keys
apiKey = os.environ.get('MAPS_API_KEY')

# instantiate the app
app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "1 per second"]
)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check route
@app.route('/ping', methods=['GET'])
@limiter.exempt
def ping_pong():
    return jsonify('pong!')

@app.route('/route', methods=['GET'])
@limiter.limit("1/minute", override_defaults=True)
def route():
    origin = request.args.get('org')
    destination = request.args.get('dest')
    waypoints = request.args.get('way')
    query = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&waypoints=optimize:true{}&key={}".format(origin, destination, waypoints, apiKey)
    r = requests.get(url = query)
    data = r.json()
    return data

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
