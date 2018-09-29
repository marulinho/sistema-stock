from __future__ import unicode_literals

import datetime
from string import lower

import null as null
import pytz
from django.db import transaction
from django.db import IntegrityError
from django.http import HttpResponse

from sistema.models import *
from sistema.utils.utils import *
from sistema.utils.constantes import *
from sistema.utils.decorators import *
from sistema.utils.error_handler import *

@transaction.atomic()
@metodos_requeridos([METODO_POST])
def registrar_categoria(request):

    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if NOMBRE in datos and not (NOMBRE == ''):
                nombre = lower(datos[NOMBRE])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_NOMBRE_CATEGORIA_FALTANTE)
            if DESCRIPCION in datos and not (DESCRIPCION == ''):
                descripcion = datos[DESCRIPCION]
            else:
                descripcion = ''
            estado_habilitado = EstadoCategoria.objects.get(nombre = ESTADO_HABILITADO)

            if Categoria.objects.filter(nombre=nombre, estado = estado_habilitado).__len__() >=1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_NOMBRE_CATEGORIA_EXISTENTE)
            else:
                categoria_creada = Categoria(nombre=nombre,
                                             descripcion=descripcion,
                                             estado=estado_habilitado)
                categoria_creada.saveNewCategoria()
                response.content = armar_response_content(None, CREACION_CATEGORIA)
                response.status_code = 200
                return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)


@transaction.atomic()
@metodos_requeridos([METODO_PUT])
def modificar_categoria(request):

    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)

        #comprobamos que vengan los datos obligatorios
        else:
            if CODIGO in datos and not (CODIGO == ''):
                codigo = datos[CODIGO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_CATEGORIA_FALTANTE)
            if NOMBRE in datos and not (NOMBRE == ''):
                nombre = lower(datos[NOMBRE])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_NOMBRE_CATEGORIA_FALTANTE)

            estado_habilitado = EstadoCategoria.objects.get(nombre = ESTADO_HABILITADO)

            if Categoria.objects.filter(codigo=codigo, estado = estado_habilitado).__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_INEXISTENTE)
            else:
                categoria_modificada = Categoria.objects.get(codigo=codigo, estado=estado_habilitado)
                if Categoria.objects.filter(nombre=nombre).exclude(codigo=categoria_modificada.codigo).__len__()>=1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_NOMBRE_CATEGORIA_EXISTENTE)
                else:
                    if DESCRIPCION in datos and not (DESCRIPCION == ''):
                        descripcion = datos[DESCRIPCION]
                        categoria_modificada.descripcion = descripcion
                    categoria_modificada.nombre = nombre
                    categoria_modificada.save()
                    response.content = armar_response_content(None, MODIFICACION_CATEGORIA)
                    response.status_code = 200
                    return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_PUT])
def eliminar_categoria(request):

    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if CODIGO in datos and not (CODIGO == ''):
                codigo = datos[CODIGO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_CATEGORIA_FALTANTE)

            estado_habilitado = EstadoCategoria.objects.get(nombre = ESTADO_HABILITADO)

            if Categoria.objects.filter(codigo=codigo, estado = estado_habilitado).__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_INEXISTENTE)
            else:
                estado_deshabilitado = EstadoCategoria.objects.get(nombre = ESTADO_DESHABILITADO)
                categoria_eliminada = Categoria.objects.get(codigo=codigo, estado=estado_habilitado)
                categoria_eliminada.estado = estado_deshabilitado
                categoria_eliminada.save()
                response.content = armar_response_content(None, ELIMINACION_CATEGORIA)
                response.status_code = 200
                return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_GET])
def obtener_categorias(request):

    try:
        response = HttpResponse()
        estado_habilitado = EstadoCategoria.objects.get(nombre = ESTADO_HABILITADO)
        if Categoria.objects.filter(estado = estado_habilitado).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CATEGORIAS_INEXISTENTES)
        else:
            categorias = Categoria.objects.filter(estado=estado_habilitado).order_by('-codigo')
            response.content = armar_response_list_content(categorias)
            response.status_code = 200
            return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_GET])
def obtener_categoria_id(request,id_categoria):

    try:
        response = HttpResponse()
        if id_categoria == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_CATEGORIA_FALTANTE)
        estado_habilitado = EstadoCategoria.objects.get(nombre = ESTADO_HABILITADO)
        if Categoria.objects.filter(codigo = id_categoria,estado = estado_habilitado).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CATEGORIA_INEXISTENTE)
        else:
            categoria = Categoria.objects.get(codigo = id_categoria, estado=estado_habilitado)
            response.content = armar_response_content(categoria)
            response.status_code = 200
            return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_PUT])
def habilitar_categoria(request):

    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()
        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if CODIGO in datos and not (CODIGO == ''):
                codigo = datos[CODIGO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_CATEGORIA_FALTANTE)
            estado_habilitado = EstadoCategoria.objects.get(nombre = ESTADO_HABILITADO)
            if Categoria.objects.filter(codigo = codigo, estado = estado_habilitado).__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CATEGORIA_HABILITADA_INEXISTENTE)
            else:
                categoria = Categoria.objects.get(codigo = codigo, estado=estado_habilitado)
                response.content = armar_response_content(categoria)
                response.status_code = 200
                return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_GET])
def obtener_subcategorias_categoria(request, id_categoria):

    try:
        response = HttpResponse()
        if id_categoria == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_CATEGORIA_FALTANTE)
        else:
            estado_habilitado = EstadoCategoria.objects.get(nombre=ESTADO_HABILITADO)
            if Categoria.objects.filter(codigo=id_categoria, estado=estado_habilitado).__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CATEGORIA_HABILITADA_INEXISTENTE)
            else:
                categoria = Categoria.objects.get(codigo=id_categoria, estado=estado_habilitado)
                response.content = armar_response_content(categoria)
                response.status_code = 200
                return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_PUT])
def desasignar_producto_categoria(request):

    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()
        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        if ID_CATEGORIA in datos and not ID_CATEGORIA == '':
            id_categoria = datos[ID_CATEGORIA]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_SUBCATEGORIA_FALTANTE)

        if ID_PRODUCTO in datos and not ID_PRODUCTO == '':
            id_producto = datos[ID_PRODUCTO]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_PRODUCTO_FALTANTE)

        estado_habilitado_categoria = EstadoCategoria.objects.get(nombre = ESTADO_HABILITADO)
        if Categoria.objects.filter(codigo = id_categoria,estado = estado_habilitado_categoria).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CATEGORIA_INEXISTENTE)

        estado_habilitado_producto = EstadoProducto.objects.get(nombre=ESTADO_HABILITADO)
        if Producto.objects.filter(codigo = id_producto,estado = estado_habilitado_producto).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PRODUCTO_INEXISTENTE)

        producto_ingresado = Producto.objects.get(codigo = id_producto,estado = estado_habilitado_producto)
        producto_ingresado.categoria = None
        producto_ingresado.save()
        response.content = armar_response_content(None,DESASIGNACION_PRODUCTO_EXITOSA)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_PUT])
def desasignar_subcategoria_categoria(request):

    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()
        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        if ID_CATEGORIA in datos and not ID_CATEGORIA == '':
            id_categoria = datos[ID_CATEGORIA]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_SUBCATEGORIA_FALTANTE)

        if ID_SUBCATEGORIA in datos and not ID_SUBCATEGORIA == '':
            id_subcategoria = datos[ID_SUBCATEGORIA]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_SUBCATEGORIA_FALTANTE)

        estado_habilitado_categoria = EstadoCategoria.objects.get(nombre = ESTADO_HABILITADO)
        if Categoria.objects.filter(codigo = id_categoria,estado = estado_habilitado_categoria).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CATEGORIA_INEXISTENTE)

        estado_habilitado_subcategoria = EstadoSubCategoria.objects.get(nombre=ESTADO_HABILITADO)
        if SubCategoria.objects.filter(codigo = id_subcategoria,estado = estado_habilitado_subcategoria).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_SUBCATEGORIA_INEXISTENTE)
        subcategoria_ingresada = SubCategoria.objects.get(codigo = id_subcategoria, estado = estado_habilitado_subcategoria)

        subcategoria_ingresada.categoria = None
        subcategoria_ingresada.save()
        response.content = armar_response_content(None,DESASIGNACION_SUBCATEGORIA_EXITOSA)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)