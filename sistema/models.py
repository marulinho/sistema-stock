# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models

# Create your models here.

class EstadoUsuario(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return "Estado Usuario: " + self.nombre

class Pregunta(models.Model):
    descripcion = models.CharField(max_length=100)
    habilitado = models.BooleanField(default=False)

    def __str__(self):
        return "Pregunta: " + self.descripcion

    def as_json(self):
        return dict (
            id_pregunta = self.id,
            descripcion = self.descripcion,
            habilitado = self.habilitado
        )

class Usuario(models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    usuario = models.CharField(max_length=40)
    contrasenia = models.CharField(max_length=40)
    fecha_desde = models.DateTimeField()
    fecha_hasta = models.DateTimeField(null=True)

    estado = models.ForeignKey(EstadoUsuario, db_column="id_estado_usuario")
    pregunta = models.ForeignKey(Pregunta, db_column='id_pregunta')

    def __str__(self):
        return 'Usuario: '+self.usuario

    def as_json(self):
        return dict(
            id_usuario = self.id,
            nombre = self.nombre,
            apellido = self.apellido,
            usuario = self.usuario,
            fecha_desde = self.fecha_desde,
            fecha_hasta = self.fecha_hasta,
            id_estado = self.estado.id,
            id_pregunta = self.pregunta.id
        )

class SesionUsuario(models.Model):
    fecha_desde = models.DateTimeField(null=True)
    fecha_hasta = models.DateTimeField(null=True)
    fecha_hasta = models.DateTimeField(null=True)

class RespuestaPregunta(models.Model):
    descripcion = models.CharField(max_length=50)

    usuario = models.ForeignKey(Usuario,db_column='id_usuario')
    pregunta = models.ForeignKey(Pregunta, db_column='id_pregunta')

    def as_json(self):
        return dict(
            id_respuesta = self.id,
            descripcion =  self.descripcion,
            id_usuario = self.usuario.id,
            id_pregunta = self.pregunta.id
        )

class HistoricoEstadoUsuario(models.Model):
    fecha_desde = models.DateTimeField()
    fecha_hasta = models.DateTimeField(null=True)

    usuario = models.ForeignKey(Usuario, db_column='id_usuario')
    estado = models.ForeignKey(EstadoUsuario, db_column='id_estado_usuario')

