# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-30 01:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfood', '0026_shoppinglist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglist',
            name='ingredients',
            field=models.TextField(blank=True, null=True),
        ),
    ]
