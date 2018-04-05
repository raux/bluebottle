# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-04 19:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payments', '0005_auto_20170919_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='DusuPayPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payments.Payment')),
                ('amount', models.CharField(blank=True, help_text=b'Amount', max_length=200, null=True)),
                ('currency', models.CharField(blank=True, default=b'USD', help_text=b'Transaction currency', max_length=200, null=True)),
                ('mobile', models.CharField(blank=True, help_text=b'Customer Phone', max_length=200, null=True)),
                ('transaction_reference', models.CharField(blank=True, help_text=b'Transaction Reference', max_length=100, null=True)),
                ('transaction_id', models.CharField(blank=True, help_text=b'Transaction ID', max_length=100, null=True)),
                ('item_id', models.CharField(blank=True, help_text=b'Item ID', max_length=200, null=True)),
                ('item_name', models.CharField(blank=True, help_text=b'Item Name', max_length=200, null=True)),
                ('customer_name', models.CharField(blank=True, help_text=b'Customer Name', max_length=200, null=True)),
                ('customer_email', models.CharField(blank=True, help_text=b'Customer Email', max_length=200, null=True)),
                ('charge', models.CharField(blank=True, help_text=b'DusuPay charge', max_length=200, null=True)),
                ('response', models.TextField(blank=True, help_text='Response from Telesom', null=True)),
                ('update_response', models.TextField(blank=True, help_text='Result from Telesom (status update)', null=True)),
            ],
            options={
                'ordering': ('-created', '-updated'),
                'verbose_name': 'Telesom/Zaad Payment',
                'verbose_name_plural': 'Telesom/Zaad Payments',
            },
            bases=('payments.payment',),
        ),
    ]
