# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-21 18:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategoria',
            name='categoria',
            field=models.ForeignKey(db_column='id_categoria', null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.Categoria'),
        ),
    ]
