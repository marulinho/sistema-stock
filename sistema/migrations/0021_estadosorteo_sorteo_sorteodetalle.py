# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-14 20:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0020_movimientostock_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoSorteo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('descripcion', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Sorteo',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('fecha_sorteo', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='SorteoDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('posicion', models.IntegerField()),
                ('ganador', models.CharField(max_length=60, null=True)),
                ('producto', models.ForeignKey(db_column='id_producto', on_delete=django.db.models.deletion.CASCADE, to='sistema.Producto')),
                ('sorteo', models.ForeignKey(db_column='id_sorteo', on_delete=django.db.models.deletion.CASCADE, to='sistema.Sorteo')),
            ],
        ),
    ]
