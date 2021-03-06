# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 01:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfood', '0013_auto_20160726_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='savedrecipe',
            name='big_image',
            field=models.TextField(default='hold', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='savedrecipe',
            name='small_image',
            field=models.TextField(default='hold', max_length=200),
            preserve_default=False,
        ),
    ]
