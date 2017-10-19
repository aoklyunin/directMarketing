# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-10-19 11:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0014_auto_20171019_1109'),
        ('consumer', '0002_auto_20171019_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tc', models.TextField(default='', max_length=100)),
                ('state', models.IntegerField(default=0)),
                ('value', models.FloatField(default=0)),
                ('dt', models.DateTimeField(default=datetime.datetime(2017, 10, 19, 11, 9, 3, 791126))),
                ('comments', models.ManyToManyField(to='mainApp.Comment')),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consumer.Consumer')),
            ],
        ),
        migrations.RenameModel(
            old_name='WorkerMarketCamp',
            new_name='ConsumerMarketCamp',
        ),
        migrations.RemoveField(
            model_name='consumertransaction',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='consumertransaction',
            name='consumer',
        ),
        migrations.DeleteModel(
            name='ConsumerTransaction',
        ),
    ]
