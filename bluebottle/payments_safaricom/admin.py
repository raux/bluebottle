from polymorphic.admin import PolymorphicChildModelAdmin

from bluebottle.payments.models import Payment
from .models import SafaricomPayment


class SafaricomPaymentAdmin(PolymorphicChildModelAdmin):
    base_model = Payment
    model = SafaricomPayment
    search_fields = ['party_a', 'transaction_reference']
    raw_id_fields = ('order_payment', )
    readonly_fields = ('amount', 'business_short_code',
                       'party_a', 'party_b', 'phone_number',
                       'account_reference', 'call_back_url',
                       'response', 'update_response')
