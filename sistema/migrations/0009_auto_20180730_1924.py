# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-30 22:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0008_auto_20180730_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caja',
            name='total_apertura',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='caja',
            name='total_cierre',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cajadetalle',
            name='total',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='combo',
            name='precio',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='combodetalle',
            name='margen_ganancia_producto_combo',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='combodetalle',
            name='precio_unitario_producto_combo',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='combodetalle',
            name='subtotal',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='listapreciodetalle',
            name='precio_unitario_compra',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='listapreciodetalle',
            name='precio_unitario_venta',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='movimientocapital',
            name='total',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='movimientostock',
            name='descuento',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='movimientostock',
            name='total_final',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='movimientostock',
            name='total_parcial',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='movimientostockdetalle',
            name='precio_unitario',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='movimientostockdetalle',
            name='subtotal',
            field=models.FloatField(),
        ),
    ]
