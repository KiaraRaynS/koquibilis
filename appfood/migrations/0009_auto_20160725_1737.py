# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 17:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appfood', '0008_auto_20160725_1729'),
    ]

    operations = [
        migrations.RenameField(
            model_name='savedrecipe',
            old_name='notes',
            new_name='note',
        ),
    ]
