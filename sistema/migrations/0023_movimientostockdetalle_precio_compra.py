# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-19 22:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0022_auto_20181014_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimientostockdetalle',
            name='precio_compra',
            field=models.FloatField(null=True),
        ),
    ]
