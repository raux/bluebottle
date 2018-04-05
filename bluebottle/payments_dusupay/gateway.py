from datetime import datetime
import hashlib
import hmac
import json
import requests


class DusuPayClient(object):
    """
    API Client for DusuPay, Uganda.
    """
    sandbox_domain = 'http://sandbox.dusupay.com/'
    live_domain = 'https://dusupay.com/'
    direct_collections_api = '/merchant-api/collections/mobile/requestPayment.json'
    transaction_status_api = '/transactions/check_status/{merchant_id}/{transaction_reference}.json'

    status_mapping = {
        ''
    }

    def __init__(self, merchant_id, merchant_key, live=False):
        """
        Initialize the client.
        """
        self.merchant_id = merchant_id
        self.merchant_key = merchant_key
        self.live = live
        self.domain = self.live_domain if live else self.sandbox_domain

    def _generate_signature(self, payload):
        message = ''.join([str(payload[k]) for k in sorted(payload.keys())])
        return hmac.new(self.merchant_key, message, hashlib.sha1).hexdigest()

    def create_payment_request(self, mobile, reference, amount, currency='UGX',
                               success_url='', item_id='', item_name='',
                               customer_name='', customer_email=''):
        """
        Create the payment with DusuPay.
        """
        timestamp = datetime.now().strftime('%s')
        url = self.domain + self.direct_collections_api

        payload = {
            "dusupay_amount": amount,
            "dusupay_currency": currency,
            "dusupay_merchantId": self.merchant_id,
            "dusupay_transactionReference": reference,
            "dusupay_customerPhone": mobile,
            "dusupay_transactionTimestamp": timestamp,
            "dusupay_successURL": success_url,
            "dusupay_itemId": item_id,
            "dusupay_itemName": item_name,
            "dusupay_customerName": customer_name,
            "dusupay_customerEmail": customer_email,
        }
        signature = self._generate_signature(payload)
        payload['signature'] = signature

        print json.dumps(payload)
        response = requests.post(url, json=payload)

        data = response.json()
        return data

    def check_transaction_status(self, transaction_reference):

        url = self.transaction_status_api.format(
            merchant_id=self.merchant_id,
            transaction_reference=transaction_reference
        )

        response = requests.get(url)
        data = response.json()
        return data
