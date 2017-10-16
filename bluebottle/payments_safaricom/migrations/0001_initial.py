# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-13 10:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payments', '0003_auto_20161025_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='SafaricomPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payments.Payment')),
                ('business_short_code', models.CharField(blank=True, help_text=b'TThe organization shortcode used to receive the transaction.', max_length=200, null=True)),
                ('transaction_type', models.CharField(blank=True, default=b'CustomerPayBillOnline', help_text=b'The transaction type to be used for this request.', max_length=200, null=True)),
                ('amount', models.CharField(blank=True, help_text=b'Amount', max_length=200, null=True)),
                ('party_a', models.CharField(blank=True, help_text=b'The MSISDN sending the funds.', max_length=100, null=True)),
                ('party_b', models.CharField(blank=True, help_text=b'The organization shortcode receiving the funds', max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, help_text=b'The MSISDN sending the funds.', max_length=100, null=True)),
                ('call_back_url', models.CharField(blank=True, help_text=b'The url to where responses from M-Pesa will be sent to.', max_length=200, null=True)),
                ('account_reference', models.CharField(blank=True, help_text='Used with M-Pesa PayBills.', max_length=200, null=True)),
                ('response', models.TextField(blank=True, help_text='Result from Safaricom (status update)', null=True)),
                ('update_response', models.TextField(blank=True, help_text='Result from Safaricom (status update)', null=True)),
            ],
            options={
                'ordering': ('-created', '-updated'),
                'verbose_name': 'Safaricom/Mpesa Payment',
                'verbose_name_plural': 'Safaricom/Mpesa Payments',
            },
            bases=('payments.payment',),
        ),
    ]
