# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-10-19 10:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0012_auto_20171019_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 19, 10, 52, 56, 477463)),
        ),
    ]
