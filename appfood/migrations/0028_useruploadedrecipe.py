# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-30 14:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appfood', '0027_auto_20160730_0101'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserUploadedRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('basic_ingredients', models.TextField()),
                ('detailed_ingredients', models.TextField(blank=True, null=True)),
                ('uploader_notes', models.TextField(blank=True, null=True)),
                ('instructions', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
