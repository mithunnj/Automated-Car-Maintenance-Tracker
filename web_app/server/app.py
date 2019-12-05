#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

# Store array of all open requests submitted through the web dashboard.
REQUESTS = []

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# GET, POST API request structure.
@app.route('/requests', methods=['GET', 'POST'])
def all_requests():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        REQUESTS.append({
            'date': post_data.get('date'),
            'mileage_miles_total': post_data.get('mileage_miles_total'),
            'mileage_kms_total': post_data.get('mileage_kms_total'),
        })
        response_object['message'] = 'Request added!'
    else:
        response_object['requests'] = REQUESTS
    return jsonify(response_object)

if __name__ == '__main__':
    # Runs server on your machine's public IP address.
    #app.run(host='0.0.0.0')

    # Runs server on the local machine's IP address.
    app.run()
