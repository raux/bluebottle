from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from bluebottle.test.utils import BluebottleAdminTestCase

from ..admin import ProjectPayoutAdmin

PROJECT_PAYOUT_FEES = {
    'beneath_threshold': 1,
    'fully_funded': 0.05,
    'not_fully_funded': 0.0725
}


class PayoutTestAdmin(BluebottleAdminTestCase):
    """ verify expected fields/behaviour is present """

    def test_extra_listfields(self):
        self.failUnless('amount_pending' in ProjectPayoutAdmin.list_display)
        self.failUnless('amount_raised' in ProjectPayoutAdmin.list_display)

    @override_settings(PROJECT_PAYOUT_FEES=PROJECT_PAYOUT_FEES)
    def test_decimal_payout_rules(self):
        # Check payout rules show decimal (if there are any)
        payout_url = reverse('admin:payouts_projectpayout_changelist')
        response = self.app.get(payout_url, user=self.superuser)
        self.failUnless('5%' in response.body)
        self.failUnless('7.25%' in response.body)
