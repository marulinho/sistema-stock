# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-25 00:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0017_auto_20180923_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='dni',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.BigIntegerField(),
        ),
    ]