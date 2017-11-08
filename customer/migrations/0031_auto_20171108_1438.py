# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-08 14:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0030_auto_20171108_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketcamp',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 8, 14, 38, 54, 89397, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='marketcamp',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 8, 14, 38, 54, 89371, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='replenishtransaction',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 8, 14, 38, 54, 87856, tzinfo=utc)),
        ),
    ]
