# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-08 15:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0030_auto_20171108_1438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumermarketcamp',
            name='cheated',
        ),
        migrations.AddField(
            model_name='consumermarketcamp',
            name='stateCheated',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='withdrawtransaction',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 8, 15, 28, 38, 866170, tzinfo=utc)),
        ),
    ]
