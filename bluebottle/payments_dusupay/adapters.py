# coding=utf-8
from bluebottle.clients import properties
from bluebottle.payments.adapters import BasePaymentAdapter
from bluebottle.payments.exception import PaymentException

from .gateway import DusuPayClient
from .models import DusupayPayment


class DusupayPaymentAdapter(BasePaymentAdapter):

    card_data = {}

    def create_payment(self):
        """
        Create a new payment
        """
        self.card_data = self.order_payment.card_data

        if 'mobile' not in self.card_data:
            raise PaymentException('Mobile is required')

        payment = DusupayPayment(order_payment=self.order_payment,
                                 mobile=self.card_data['mobile'])
        payment.amount = int(self.order_payment.amount.amount)
        payment.currency = str(self.order_payment.amount.currency)
        payment.transaction_reference = self.order_payment.id

        gateway = DusuPayClient(
            self.credentials['merchant_id'],
            self.credentials['merchant_key'],
            properties.LIVE_PAYMENTS_ENABLED
        )
        customer_name = ''
        customer_email = ''
        if payment.order_payment.order.user:
            customer_name = payment.order_payment.order.user.full_name
            customer_email = payment.order_payment.order.user.email
        response = gateway.create_payment_request(
            mobile=payment.mobile,
            reference=payment.order_payment.id,
            amount=payment.amount,
            currency=payment.currency,
            success_url='',
            item_id=payment.order_payment.id,
            item_name=payment.order_payment.order.donations.first().project.title,
            customer_name=customer_name,
            customer_email=customer_email
        )
        # payment.transaction_reference = response['payment_id']
        # payment.status = response['status']
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

    def check_payment_status(self):
        if self.payment.status == 'settled':
            return

        if self.order_payment.authorization_action:
            self.order_payment.authorization_action.delete()

        action = self.get_authorization_action()
        self.order_payment.set_authorization_action(action)
        self.order_payment.save()
