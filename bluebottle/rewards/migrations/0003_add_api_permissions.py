# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-08-04 09:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rewards', '0002_auto_20160720_2245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reward',
            options={'ordering': ['-project__created', 'amount'], 'permissions': (('api_read_reward', 'Can view reward through the API'), ('api_add_reward', 'Can add reward through the API'), ('api_change_reward', 'Can change reward through the API'), ('api_delete_reward', 'Can delete reward through the API')), 'verbose_name': 'Gift', 'verbose_name_plural': 'Gifts'},
        ),
    ]