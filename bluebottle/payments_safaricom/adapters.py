# coding=utf-8
from bluebottle.payments.exception import PaymentException
from django.db import connection

from bluebottle.payments.adapters import BasePaymentAdapter
from bluebottle.payments_safaricom.models import SafaricomPayment

from mpesa.services import PaymentService


class SafaricomPaymentAdapter(BasePaymentAdapter):
    MODEL_CLASSES = [SafaricomPayment]

    card_data = {}

    def create_payment(self):
        """
        Create a new payment
        """
        self.card_data = self.order_payment.card_data

        if 'mobile' not in self.card_data:
            raise PaymentException('Mobile is required')

        payment = SafaricomPayment(order_payment=self.order_payment, mobile=self.card_data['mobile'])
        payment.amount = int(self.order_payment.amount.amount)

        if str(self.order_payment.amount.currency) != 'KES':
            raise PaymentException('You should pick KES as a currency to use Safaricom/Mpesa')

        service = PaymentService(
            merchant_id=self.credentials['merchant_id'],
            merchant_passkey=self.credentials['merchant_passkey']
        )

        tenant = connection.tenant
        payment.description = '{0}-{1}'.format(tenant.name, self.order_payment.id)

        response = service.checkout_request(
            merchant_transaction_id=None,
            reference_id=None,
            msisdn=None,
            amount=None,
            enc_params=None,
            callback_url=None
        )

        payment.transaction_reference = response['payment_id']
        payment.status = response['status']
        payment.response = response['response']
        payment.save()

        self.payment = payment
        # Check status right away so the payment gets processed
        self.check_payment_status()
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
                    'method': 'telesom-sms',
                    'text': 'Confirm the payment by SMS'
                }
            }
        else:
            reply = self.payment.update_response
            raise PaymentException("Error processing Telesom/Zaad transaction. {0}".format(reply))
