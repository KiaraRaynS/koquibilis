# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-02 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfood', '0036_userpage_bookmarks_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='useruploadedrecipe',
            name='recipe_link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
