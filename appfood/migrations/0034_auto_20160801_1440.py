# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 14:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appfood', '0033_useruploadedrecipe_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useruploadedrecipe',
            old_name='photo',
            new_name='recipephoto',
        ),
    ]
