import factory
from moneyed.classes import Money, UGX

from bluebottle.test.factory_models.payments import OrderPaymentFactory, OrderFactory

from ..models import DusuPayPayment


class DusuPayOrderFactory(OrderFactory):
    total = Money(10, UGX)


class DusuPayOrderPaymentFactory(OrderPaymentFactory):
    payment_method = 'dusupayMtn'
    order = factory.SubFactory(DusuPayOrderFactory)
    amount = Money(2000, UGX)


class DusuPayPaymentFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = DusuPayPayment
    order_payment = factory.SubFactory(DusuPayOrderPaymentFactory)
