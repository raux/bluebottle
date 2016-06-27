# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-23 13:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payments', '0001_initial'),
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='remotedocdatapayment',
            name='local_payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.Payment'),
        ),
        migrations.AddField(
            model_name='remotedocdatapayment',
            name='remote_payout',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounting.RemoteDocdataPayout'),
        ),
        migrations.AddField(
            model_name='banktransaction',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounting.BankTransactionCategory'),
        ),
    ]