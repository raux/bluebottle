# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-23 13:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bb_payouts', '0001_initial'),
        ('payouts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectpayoutlog',
            name='payout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payout_logs', to='payouts.ProjectPayout'),
        ),
        migrations.AddField(
            model_name='organizationpayoutlog',
            name='payout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payout_logs', to='payouts.OrganizationPayout'),
        ),
    ]
