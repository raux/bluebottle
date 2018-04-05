from django.conf.urls import url

from ..views import PaymentResponseView

urlpatterns = [
    url(r'^payment_response/$',
        PaymentResponseView.as_view(),
        name='dusupay-payment-response'),
]
