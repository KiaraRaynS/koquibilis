# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfood', '0019_auto_20160727_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
