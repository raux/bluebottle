from polymorphic.admin import PolymorphicChildModelAdmin

from bluebottle.payments.models import Payment
from .models import DusupayPayment


class DusupayPaymentAdmin(PolymorphicChildModelAdmin):
    base_model = Payment
    model = DusupayPayment
    search_fields = ['mobile', 'transaction_reference']
    raw_id_fields = ('order_payment', )
    readonly_fields = ('amount', 'currency', 'mobile',

                       'transaction_reference',
                       'response', 'update_response')
