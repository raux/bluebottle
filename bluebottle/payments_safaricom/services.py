import base64
from hashlib import sha256

import requests
from django.utils.timezone import now


class SafaricomService(object):

    test_server = "https://sandbox.safaricom.co.ke"
    live_server = "https://safaricom.co.ke"

    server = live_server

    access_token_path = '/oauth/v1/generate?grant_type=client_credentials'
    process_request_path = '/mpesa/stkpush/v1/processrequest'
    balance_request_path = '/mpesa/accountbalance/v1/query'

    short_code = ''

    demo = False

    access_token = None

    def __init__(self, consumer_key, consumer_password, short_code, demo=False):
        self.consumer_key = consumer_key
        self.consumer_password = consumer_password
        self.short_code = short_code
        self.demo = demo
        if demo:
            self.server = self.test_server
            self.short_code = '174379'

    def get_access_token(self):
        url = self.server + self.access_token_path
        response = requests.get(url, auth=(self.consumer_key, self.consumer_password))
        data = response.json()
        self.access_token = data['access_token']
        return self.access_token

    def _generate_password(self, timestamp):
        string = self.short_code + self.consumer_password + timestamp
        return base64.b64encode(sha256(string).hexdigest().upper())

    def process_request(self, phone_number=None, amount=None,
                        callback_url=None, reference=None, description=None):

        headers = {"Authorization": "Bearer %s" % self.get_access_token()}
        timestamp = now().strftime('%Y%m%d%H%M%S')
        request = {
            "BusinessShortCode": self.short_code,
            "Password": self._generate_password(timestamp),
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": " ",
            "PartyB": " ",
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": " ",
            "TransactionDesc": " "
        }
        url = self.server + self.process_request_path
        response = requests.post(url, request, headers=headers)
        return response.json()
