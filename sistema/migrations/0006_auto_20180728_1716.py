# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-28 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0005_auto_20180728_1707'),
    ]

    operations = [
        migrations.RenameField(
            model_name='combodetalle',
            old_name='precio_producto_combo',
            new_name='precio_unitario_producto_combo',
        ),
        migrations.AddField(
            model_name='combodetalle',
            name='subtotal',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
