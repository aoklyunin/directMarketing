# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-10-20 14:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0016_auto_20171020_1430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumer',
            name='autoVKRepost',
        ),
        migrations.AlterField(
            model_name='withdrawtransaction',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 20, 14, 43, 12, 759350)),
        ),
    ]
