# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-01-23 08:14
from __future__ import unicode_literals

import bluebottle.utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0066_auto_20180121_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcreatetemplate',
            name='sub_name',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectcreatetemplate',
            name='default_amount_asked',
            field=bluebottle.utils.fields.MoneyField(blank=True, currency_choices="[('EUR', u'Euro')]", decimal_places=2, default=None, max_digits=12, null=True),
        ),
    ]
