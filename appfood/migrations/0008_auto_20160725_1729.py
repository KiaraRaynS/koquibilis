# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 17:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appfood', '0007_userpage_userhandle'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('ingredients', models.TextField()),
                ('notes', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appfood.UserPage')),
            ],
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='allergens',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.TextField(default='hold'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Allergen',
        ),
        migrations.DeleteModel(
            name='Ingredient',
        ),
    ]
