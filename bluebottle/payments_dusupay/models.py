from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext as _

from bluebottle.payments.models import Payment


class DusupayPayment(Payment):

    amount = models.CharField(
        help_text="Amount",
        null=True, blank=True,
        max_length=200)
    currency = models.CharField(
        help_text="Transaction currency",
        default="USD",
        null=True, blank=True,
        max_length=200)
    mobile = models.CharField(
        help_text="Customer Phone",
        null=True, blank=True,
        max_length=200)
    transaction_reference = models.CharField(
        help_text="Transaction Reference",
        null=True, blank=True,
        max_length=100)
    transaction_id = models.CharField(
        help_text="Transaction ID",
        null=True, blank=True,
        max_length=100)

    item_id = models.CharField(
        help_text="Item ID",
        null=True, blank=True,
        max_length=200)
    item_name = models.CharField(
        help_text="Item Name",
        null=True, blank=True,
        max_length=200)
    customer_name = models.CharField(
        help_text="Customer Name",
        null=True, blank=True,
        max_length=200)
    customer_email = models.CharField(
        help_text="Customer Email",
        null=True, blank=True,
        max_length=200)
    charge = models.CharField(
        help_text="DusuPay charge",
        null=True, blank=True,
        max_length=200)

    response = models.TextField(
        help_text=_('Response from Telesom'),
        null=True, blank=True)
    update_response = models.TextField(
        help_text=_('Result from Telesom (status update)'),
        null=True, blank=True)

    class Meta:
        ordering = ('-created', '-updated')
        verbose_name = "Dusupay MTN/AirTel Payment"
        verbose_name_plural = "Dusupay MTN/AirTel Payments"

    def get_method_name(self):
        """ Return the payment method name."""
        return 'dusupay'

    def get_fee(self):
        """
        Not sure about the fee yet.
        """
        fee = round(self.order_payment.amount * Decimal(0.05), 2)
        return fee
