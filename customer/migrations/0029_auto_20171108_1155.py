# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-08 11:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0028_auto_20171108_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketcamp',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 8, 11, 55, 7, 881686, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='marketcamp',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 8, 11, 55, 7, 881656, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='replenishtransaction',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 8, 11, 55, 7, 880157, tzinfo=utc)),
        ),
    ]
