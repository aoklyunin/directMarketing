# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-10-19 17:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0005_auto_20171019_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawtransaction',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 19, 17, 27, 30, 202897)),
        ),
    ]
