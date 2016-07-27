# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 12:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appfood', '0014_auto_20160727_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
