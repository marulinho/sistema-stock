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

class EstadoCombo(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return "Estado Combo: " + self.nombre



class Combo(models.Model):
    codigo = models.IntegerField(primary_key=True, default=1000)
    nombre = models.CharField(max_length=60)
    precio = models.IntegerField()

    estado = models.ForeignKey(EstadoCombo, db_column = 'id_estado_combo')

    def as_json(self):
        return dict(
            codigo = self.codigo,
            nombre = self.nombre,
            precio = self.precio,
            id_estado = self.estado.id
        )

    def saveNewCombo(self):
        if Combo.objects.order_by('codigo').__len__()==0:
            self.codigo = 1000
        else:
            self.codigo = Combo.objects.order_by('codigo').last().codigo + 1
        super(Combo, self).save()

class ComboDetalle(models.Model):
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto, db_column='id_producto')
    precio_unitario_producto_combo = models.IntegerField()
    subtotal = models.IntegerField()
    combo = models.ForeignKey(Combo, db_column='id_combo')

    def as_json(self):
        return dict(
            cantidad = self.cantidad,
            precio_producto_combo = self.precio_producto_combo,
            producto = self.producto.as_json(),
            combo = self.combo.codigo
        )

class EstadoListaPrecio(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return "Estado Lista de Precio: " + self.nombre



class ListaPrecio(models.Model):
    codigo = models.IntegerField(primary_key=True, default=1000)
    nombre = models.CharField(max_length=60)
    vigencia_desde = models.DateTimeField(null=False)
    vigencia_hasta = models.DateTimeField(null=True)

    estado = models.ForeignKey(EstadoListaPrecio, db_column = 'id_estado_lista_precio')

    def as_json(self):
        return dict(
            codigo = self.codigo,
            nombre = self.nombre,
            vigencia_desde = self.vigencia_desde,
            vigencia_hasta=self.vigencia_hasta,
            id_estado = self.estado.id
        )

    def saveNewListaPrecio(self):
        if ListaPrecio.objects.order_by('codigo').__len__()==0:
            self.codigo = 1000
        else:
            self.codigo = ListaPrecio.objects.order_by('codigo').last().codigo + 1
        super(ListaPrecio, self).save()

class ListaPrecioDetalle(models.Model):
    precio_unitario_compra = models.IntegerField()
    precio_unitario_venta = models.IntegerField()

    lista_precio = models.ForeignKey(ListaPrecio, db_column= 'id_lista_precio')
    producto = models.ForeignKey(Producto, db_column='id_producto')


    def as_json(self):
        return dict(
            precio_unitario_compra = self.precio_unitario_compra,
            precio_unitario_venta = self.precio_unitario_venta,
            producto = self.producto.as_json(),
            lista_precio = self.lista_precio.as_json()
        )