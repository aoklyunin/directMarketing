# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-10-23 12:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0031_auto_20171021_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 23, 12, 6, 17, 481415)),
        ),
    ]
