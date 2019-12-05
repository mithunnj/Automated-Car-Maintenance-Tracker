#!/usr/bin/env python3

'''
This file will handle all aspects of recieving and storing MMS using the Twilio module.
'''

from twilio.rest import Client
import os
import sys
import json
import requests
import datetime

# Coloured text
CGREEN = '\33[32m'
CRED = '\33[31m'
CEND = '\033[0m'

# Load environment variables used to store sensitive information.
try:
    SID = os.environ['SID']
    TOKEN = os.environ['TOKEN']
    TO_NUM = os.environ['TO_NUM']
    FROM_NUM = os.environ['FROM_NUM']
except Exception as e:
    sys.exit(CRED + 'Make sure env variables: SID, TOKEN, TO_NUM, FROM_NUM is set. Exit with the following error: ' + str(e) + CEND)

def request_mileage():
    '''
    Input: None
    Output: None

    Description: This is the text that will be ask the user for an image of the mileage.
    '''
    account_sid = SID
    auth_token = TOKEN
    client = Client(account_sid, auth_token)
    today = datetime.datetime.now().strftime("%F")

    try:
        message = client.messages \
                .create(
                        body="Maintenance Notification! - Please send picture of mileage for {}".format(today),
                        from_=FROM_NUM,
                        to=TO_NUM
                    )
        print('\n' + CGREEN + 'Successfully sent text message.' + CEND + '\n')
    except Exception as e:
        print('\n' + CRED + 'Failed to send text message, with error: ' + e + CEND + '\n')

def post_request(miles, kms):
    '''
    Input: <str> miles, kms : The mileage information in both units of measurement.
    Output: None

    Description: Given the mileage information in miles and kms, submit a POST request to the backend server API to store this information.
    '''
    
    payload = {
        'date': str(datetime.datetime.now()),
        'mileage_miles_total': miles,
        'mileage_kms_total': kms
    }
    header_content = {'Content-type': 'application/json'}
    r = requests.post("http://localhost:5000/requests", data=json.dumps(payload), headers=header_content, verify=False)
    if r.status_code != 200:
        print('\n' + CRED + 'POST request error: {}'.format(r.status_code) + CEND + '\n')
        sys.exit('Fix backend API server, then proceed.')
    else:
        print('\n' + CGREEN + 'Successfully submitted a POST request to the server!' + CEND + '\n')

    return



