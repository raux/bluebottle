# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-01-18 11:17
from __future__ import unicode_literals

import bluebottle.utils.fields
from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0059_auto_20180118_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectcreatetemplate',
            name='amount',
            field=bluebottle.utils.fields.MoneyField(currency_choices="[('EUR', u'Euro')]", decimal_places=2, default=Decimal('0.0'), max_digits=12),
        ),
        migrations.AlterField(
            model_name='projectcreatetemplate',
            name='amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[(b'EUR', 'Euro')], default='EUR', editable=False, max_length=3),
        ),
    ]