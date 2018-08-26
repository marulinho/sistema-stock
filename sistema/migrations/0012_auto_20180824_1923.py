# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-24 22:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0011_auto_20180814_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipomovimientocapital',
            name='estado',
        ),
        migrations.AddField(
            model_name='movimientocapital',
            name='descripcion_movimiento',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movimientocapital',
            name='forma_pago',
            field=models.ForeignKey(db_column='id_forma_pago', default=1, on_delete=django.db.models.deletion.CASCADE, to='sistema.FormaPago'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movimientocapital',
            name='estado',
            field=models.ForeignKey(db_column='id_estado', on_delete=django.db.models.deletion.CASCADE, to='sistema.EstadoMovimientoCapital'),
        ),
        migrations.AlterField(
            model_name='movimientostock',
            name='total_final',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='movimientostock',
            name='total_parcial',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='movimientostockdetalle',
            name='precio_unitario',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='movimientostockdetalle',
            name='subtotal',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='stock_minimo',
            field=models.IntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='EstadoTipoMovimientoCapital',
        ),
    ]
