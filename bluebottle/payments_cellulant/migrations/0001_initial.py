# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-06-27 12:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payments', '0005_auto_20170919_1621'),
        ('projects', '0078_auto_20180528_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='CellulantPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payments.Payment')),
                ('reference', models.CharField(blank=True, help_text=b'Transaction reference', max_length=200, null=True)),
                ('msisdn', models.CharField(blank=True, help_text=b'Cellulant msisdn (phone number)', max_length=200, null=True)),
                ('account_number', models.CharField(blank=True, help_text=b'Cellulant account number', max_length=200, null=True)),
                ('amount', models.CharField(blank=True, help_text=b'Cellulant amount', max_length=200, null=True)),
                ('currency', models.CharField(blank=True, help_text=b'Cellulant currency code', max_length=200, null=True)),
                ('country_code', models.CharField(blank=True, help_text=b'Cellulant country code', max_length=200, null=True)),
                ('payment_method', models.CharField(blank=True, help_text=b'Cellulant payment method', max_length=200, null=True)),
                ('language', models.CharField(blank=True, help_text=b'Cellulant language code', max_length=200, null=True)),
                ('payment_option', models.CharField(blank=True, help_text=b'Cellulant payment option', max_length=200, null=True)),
                ('payment_mode', models.CharField(blank=True, help_text=b'Cellulant payment mode', max_length=200, null=True)),
                ('callback_url', models.CharField(blank=True, help_text=b'Cellulant callback url', max_length=200, null=True)),
                ('response', models.TextField(blank=True, help_text='Response from Cellulant', null=True)),
                ('update_response', models.TextField(blank=True, help_text='Result from Cellulant (status update)', null=True)),
            ],
            options={
                'ordering': ('-created', '-updated'),
                'verbose_name': 'Cellulant Payment',
                'verbose_name_plural': 'Cellulant Payments',
            },
            bases=('payments.payment',),
        ),
        migrations.CreateModel(
            name='CellulantProject',
            fields=[
                ('projectaddon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='projects.ProjectAddOn')),
                ('account_number', models.CharField(blank=True, help_text=b'Cellulant account number', max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('projects.projectaddon',),
        ),
    ]
