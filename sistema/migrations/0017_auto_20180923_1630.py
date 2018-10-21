# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-23 19:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0016_auto_20180923_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipocliente',
            name='estado',
            field=models.ForeignKey(db_column='id_estado', default=1000, on_delete=django.db.models.deletion.CASCADE, to='sistema.EstadoTipoCliente'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='dni',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.IntegerField(),
        ),
    ]