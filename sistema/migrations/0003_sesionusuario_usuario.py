# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-26 01:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0002_auto_20180625_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='sesionusuario',
            name='usuario',
            field=models.ForeignKey(db_column='id_usuario', default=0, on_delete=django.db.models.deletion.CASCADE, to='sistema.Usuario'),
            preserve_default=False,
        ),
    ]
