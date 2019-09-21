# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-09-21 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_auto_20190921_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default='qwer', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='clist',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='mobile',
            field=models.CharField(default=123456, max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='receiver',
            field=models.CharField(default='recevier', max_length=32),
            preserve_default=False,
        ),
    ]
