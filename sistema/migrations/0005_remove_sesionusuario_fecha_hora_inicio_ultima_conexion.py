# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-26 01:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0004_auto_20180625_2246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sesionusuario',
            name='fecha_hora_inicio_ultima_conexion',
        ),
    ]
