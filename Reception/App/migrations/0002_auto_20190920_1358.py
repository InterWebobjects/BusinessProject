# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-09-20 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commodity',
            name='is_delete',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='is_delete',
            field=models.BooleanField(default=0),
        ),
    ]
