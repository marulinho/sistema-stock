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
    key_session = models.UUIDField(primary_key = True, default = uuid.uuid4, editable= False)
    fecha_hora_desde = models.DateTimeField(null=True)
    fecha_hora_hasta = models.DateTimeField(null=True)

    usuario = models.ForeignKey(Usuario, db_column='id_usuario')

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


class EstadoCategoria(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return "Estado Categoria: " + self.nombre


class Categoria(models.Model):
    codigo = models.IntegerField(primary_key=True, default=1000)
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=50, null=True)

    estado = models.ForeignKey(EstadoCategoria, db_column="id_estado_categoria")

    def as_json(self):
        return dict(
            codigo=self.codigo,
            nombre=self.nombre,
            descripcion=self.descripcion,
            estado=self.estado.id
        )

    def saveNewCategoria(self):
        if Categoria.objects.order_by('codigo').__len__()==0:
            self.codigo = 1000
        else:
            self.codigo = Categoria.objects.order_by('codigo').last().codigo + 1
        super(Categoria, self).save()
class EstadoSubCategoria(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return "Estado SubCategoria: " + self.nombre

class SubCategoria(models.Model):
    codigo = models.IntegerField(primary_key=True, default=1000)
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=50, null=True)

    estado = models.ForeignKey(EstadoSubCategoria, db_column = 'id_estado_subcategoria')
    categoria = models.ForeignKey(Categoria, db_column = 'id_categoria', null=True)

    def as_json(self):
        return dict(
            codigo = self.codigo,
            nombre = self.nombre,
            descripcion = self.descripcion,
            id_estado = self.estado.id
        )

    def saveNewSubCategoria(self):
        if SubCategoria.objects.order_by('codigo').__len__()==0:
            self.codigo = 1000
        else:
            self.codigo = SubCategoria.objects.order_by('codigo').last().codigo + 1
        super(SubCategoria, self).save()
class EstadoUnidadMedida(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return "Estado Unidad Medida: " + self.nombre

class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)
    fecha_desde = models.DateTimeField()
    fecha_hasta = models.DateTimeField(null=True)

    estado = models.ForeignKey(EstadoUnidadMedida, db_column='id_estado_unidad_medidad')

    def as_json(self):
        return dict(
            id_unidad_medida = self.id,
            id_estado_unidad_medida = self.estado.id,
            nombre = self.nombre,
            descripcion = self.descripcion
        )

    def __str__(self):
        return "Unidad Medida: " + self.nombre

class EstadoProducto(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return "Estado Producto: " + self.nombre


class Producto(models.Model):
    codigo = models.IntegerField(primary_key=True, default=1000)
    nombre = models.CharField(max_length=60)
    marca = models.CharField(max_length=60)
    medida = models.IntegerField()
    stock_local = models.IntegerField(null = True)
    stock_deposito = models.IntegerField(null=True)

    unidad_medida = models.ForeignKey(UnidadMedida, db_column='id_unidad_medida')
    estado = models.ForeignKey(EstadoProducto, db_column = 'id_estado_producto')
    categoria = models.ForeignKey(Categoria, db_column = 'id_categoria', null=True)
    subcategoria = models.ForeignKey(SubCategoria, db_column = 'id_subcategoria', null=True)

    def as_json(self):
        return dict(
            codigo = self.codigo,
            nombre = self.nombre,
            marca = self.marca,
            medida = self.medida,
            stock_local = self.stock_local,
            stock_deposito = self.stock_deposito,
            id_unidad_medida = self.unidad_medida.id,
            nombre_unidad_medida = self.unidad_medida.nombre,
            id_estado = self.estado.id
        )

    def saveNewProducto(self):
        if Producto.objects.order_by('codigo').__len__()==0:
            self.codigo = 1000
        else:
            self.codigo = Producto.objects.order_by('codigo').last().codigo + 1
        super(Producto, self).save()

