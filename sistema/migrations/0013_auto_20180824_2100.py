# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-25 00:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0012_auto_20180824_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caja',
            name='fecha_cierre',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='caja',
            name='total_cierre',
            field=models.FloatField(null=True),
        ),
    ]