# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfood', '0017_fooditem_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='quantity',
            field=models.IntegerField(default=1, max_length=15),
            preserve_default=False,
        ),
    ]
