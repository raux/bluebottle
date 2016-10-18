# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-20 20:45
from __future__ import unicode_literals

import bluebottle.utils.fields
from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payments_manual', '0002_auto_20160627_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='manualpayment',
            name='amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[(b'EUR', b'Euro')], default=b'EUR', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='manualpayment',
            name='amount',
            field=bluebottle.utils.fields.MoneyField(currency_choices=[(b'EUR', b'Euro')], decimal_places=2, default=Decimal('0.0'), default_currency=b'EUR', editable=False, max_digits=12, verbose_name='amount'),
        ),
    ]