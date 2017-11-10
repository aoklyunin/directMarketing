# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-09 15:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0033_auto_20171109_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawtransaction',
            name='paymentComment',
            field=models.TextField(blank=True, default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='withdrawtransaction',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 9, 15, 46, 17, 84494, tzinfo=utc)),
        ),
    ]