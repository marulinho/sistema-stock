# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-15 02:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0010_producto_stock_minimo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipomovimientostock',
            name='estado',
        ),
        migrations.DeleteModel(
            name='EstadoTipoMovimientoStock',
        ),
    ]
