# coding=utf-8
from bluebottle.payments.exception import PaymentException
from django.db import connection

from bluebottle.clients import properties
from bluebottle.payments.adapters import BasePaymentAdapter
from bluebottle.payments_safaricom.models import SafaricomPayment

from .services import SafaricomService


class SafaricomPaymentAdapter(BasePaymentAdapter):
    MODEL_CLASSES = [SafaricomPayment]

    card_data = {}

    def _load_service(self):
        return SafaricomService(
            consumer_key=self.credentials['consumer_key'],
            consumer_password=self.credentials['consumer_password'],
            shortcode=self.credentials['shortcode'],
            passphrase=self.credentials['passphrase'],
            live=properties.LIVE_PAYMENTS_ENABLED
        )

    def create_payment(self):
        """
        Create a new payment
        """
        self.card_data = self.order_payment.card_data

        if 'msidn' not in self.card_data:
            raise PaymentException('MSIDN is required')

        payment = SafaricomPayment(order_payment=self.order_payment, party_a=self.card_data['msidn'])

        payment.amount = int(self.order_payment.amount.amount)
        payment.business_short_code = self.credentials['shortcode']
        payment.party_b = self.credentials['shortcode']
        payment.phone_number = self.card_data['msidn']
        payment.call_back_url = 'http://example.com'

        if str(self.order_payment.amount.currency) != 'KES':
            raise PaymentException('You should pick KES as a currency to use Safaricom/Mpesa')

        service = self._load_service()

        tenant = connection.tenant
        payment.description = '{0}-{1}'.format(tenant.name, self.order_payment.id)

        payment.status = 'started'
        payment.save()

        response = service.process_request(
            phone_number=payment.party_a,
            amount=self.order_payment.amount.amount,
            callback_url=payment.call_back_url,
            reference=self.order_payment.id,
            description='Donation'
        )

        payment.account_reference = response['request_id']
        payment.status = response['status']
        payment.response = response['response']
        payment.save()

        if payment.status == 'failed':
            raise PaymentException("Error processing Safaricom/MPESA transaction. {0}".format(response['error']))

        self.payment = payment

        return payment

    def get_authorization_action(self):
        """
        Handle payment
        """

        if self.payment.status == 'settled':
            return {'type': 'success'}
        elif self.payment.status == 'started':
            return {
                'type': 'step2',
                'payload': {
                    'method': 'mpesa-confirm',
                    'text': 'Confirm the payment through your M-PESA App'
                }
            }
        else:
            reply = self.payment.update_response
            raise PaymentException("Error processing Safaricom/MPESA transaction. {0}".format(reply))

    def check_payment_status(self):
        service = self._load_service()
        payment = self.payment

        response = service.query_request(
            request_id=payment.account_reference
        )

        payment.status = response['status']
        payment.update_response = response['response']
        payment.save()

        if payment.status == 'failed':
            raise PaymentException("Error processing Safaricom/MPESA transaction. {0}".format(response['error']))

        action = self.get_authorization_action()
        self.order_payment.set_authorization_action(action)
        self.order_payment.save()
