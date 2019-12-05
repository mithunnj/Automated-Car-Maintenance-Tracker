#!/usr/bin/env python3

import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import sys

#NOTE: This variable used to be called DOWNLOAD_DIRECTORY
IMAGE_DIRECTORY = '../images'
app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming with a simple text message."""

    resp = MessagingResponse()

    if request.values['NumMedia'] != '0':

        # Use the message SID as a filename.
        filename = request.values['MessageSid'] + '.JPG'
        with open('{}/{}'.format(IMAGE_DIRECTORY, filename), 'wb') as f:
           image_url = request.values['MediaUrl0']
           f.write(requests.get(image_url).content)

        resp.message("Image of mileage was processed successfully - Thank you!")
    else:
        resp.message("Try sending the picture again!")

    return str(resp)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="localhost", port=80, debug=True)