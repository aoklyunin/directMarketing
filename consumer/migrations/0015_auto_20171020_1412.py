# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-10-20 14:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0014_auto_20171020_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawtransaction',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 20, 14, 12, 52, 148168)),
        ),
    ]
