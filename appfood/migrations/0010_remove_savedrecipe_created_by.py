# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-26 00:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appfood', '0009_auto_20160725_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savedrecipe',
            name='created_by',
        ),
    ]
