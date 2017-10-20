# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-10-20 11:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_auto_20171019_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketcamp',
            name='adminApproved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='marketcamp',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 20, 11, 53, 24, 963301)),
        ),
        migrations.AlterField(
            model_name='marketcamp',
            name='image',
            field=models.ImageField(default='template.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='marketcamp',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 20, 11, 53, 24, 963271)),
        ),
        migrations.AlterField(
            model_name='replenishtransaction',
            name='dt',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 20, 11, 53, 24, 961530)),
        ),
    ]
