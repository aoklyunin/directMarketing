# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-10-21 11:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0020_auto_20171021_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketcamp',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 21, 11, 24, 35, 855934)),
        ),
        migrations.AlterField(
            model_name='marketcamp',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 21, 11, 24, 35, 855905)),
        ),
        migrations.AlterField(
            model_name='replenishtransaction',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 21, 11, 24, 35, 854083)),
        ),
    ]