# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfood', '0032_auto_20160801_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='useruploadedrecipe',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos'),
        ),
    ]
