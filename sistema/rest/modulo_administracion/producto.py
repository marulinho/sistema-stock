from __future__ import unicode_literals

import datetime
from string import lower

import pytz
from django.db import transaction
from django.db import IntegrityError

from sistema.models import *
from sistema.utils.utils import *
from sistema.utils.constantes import *
from sistema.utils.decorators import *
from sistema.utils.error_handler import *

@transaction.atomic()
@metodos_requeridos([METODO_POST])
def registrar_producto(request):

    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if NOMBRE in datos and not (NOMBRE == ''):
                nombre = lower(datos[NOMBRE])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_NOMBRE_PRODUCTO_FALTANTE)
            if MARCA in datos and not (MARCA == ''):
                marca = lower(datos[MARCA])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_MARCA_PRODUCTO_FALTANTE)
            if MEDIDA in datos and not (MEDIDA == ''):
                medida = datos[MEDIDA]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_MEDIDA_PRODUCTO_FALTANTE)
            if ID_UNIDAD_MEDIDA in datos and not (ID_UNIDAD_MEDIDA == ''):
                id_unidad_medida = datos[ID_UNIDAD_MEDIDA]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_UNIDAD_MEDIDA_PRODUCTO_FALTANTE)
            if STOCK_MINIMO in datos and not (STOCK_MINIMO == ''):
                stock_minimo = datos[STOCK_MINIMO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_STOCK_MINIMO_PRODUCTO_FALTANTE)
            if stock_minimo <=0:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_STOCK_MINIMO_PRODUCTO_INSUFICIENTE)

            estado_habilitado_unidad_medida = EstadoUnidadMedida.objects.get(nombre = ESTADO_HABILITADO)

            if UnidadMedida.objects.filter(id=id_unidad_medida,
                                           estado = estado_habilitado_unidad_medida).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_UNIDAD_MEDIDA_PRODUCTO_INEXISTENTE)

            unidad_medida = UnidadMedida.objects.get(id = id_unidad_medida,
                                                     estado = estado_habilitado_unidad_medida)

            estado_habilitado_producto = EstadoProducto.objects.get(nombre = ESTADO_HABILITADO)

            if Producto.objects.filter(nombre=nombre,
                                       marca = marca,
                                       medida = medida,
                                       unidad_medida = unidad_medida,
                                       estado = estado_habilitado_producto).__len__() >=1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PRODUCTO_EXISTENTE)
            else:
                producto_creado = Producto( nombre = nombre,
                                            marca = marca,
                                            medida = medida,
                                            unidad_medida = unidad_medida,
                                            stock_deposito= 0,
                                            stock_local= 0,
                                            stock_minimo = stock_minimo,
                                            estado = estado_habilitado_producto)
                producto_creado.saveNewProducto()
                response.content = armar_response_content(None, CREACION_PRODUCTO)
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
def modificar_producto(request):

    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if CODIGO in datos and not (CODIGO == ''):
                codigo = datos[CODIGO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_PRODUCTO_FALTANTE)
            if NOMBRE in datos and not (NOMBRE == ''):
                nombre = lower(datos[NOMBRE])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_NOMBRE_PRODUCTO_FALTANTE)
            if MARCA in datos and not (MARCA == ''):
                marca = lower(datos[MARCA])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_MARCA_PRODUCTO_FALTANTE)
            if MEDIDA in datos and not (MEDIDA == ''):
                medida = datos[MEDIDA]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_MEDIDA_PRODUCTO_FALTANTE)
            if ID_UNIDAD_MEDIDA in datos and not (ID_UNIDAD_MEDIDA == ''):
                id_unidad_medida = datos[ID_UNIDAD_MEDIDA]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_UNIDAD_MEDIDA_PRODUCTO_FALTANTE)
            if STOCK_MINIMO in datos and not (STOCK_MINIMO == ''):
                stock_minimo = datos[STOCK_MINIMO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_STOCK_MINIMO_PRODUCTO_FALTANTE)
            if stock_minimo <=0:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_STOCK_MINIMO_PRODUCTO_INSUFICIENTE)


            estado_habilitado_unidad_medida = EstadoUnidadMedida.objects.get(nombre = ESTADO_HABILITADO)

            if UnidadMedida.objects.filter(id=id_unidad_medida,
                                           estado = estado_habilitado_unidad_medida).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_UNIDAD_MEDIDA_PRODUCTO_INEXISTENTE)

            unidad_medida = UnidadMedida.objects.get(id = id_unidad_medida,
                                                     estado = estado_habilitado_unidad_medida)

            estado_habilitado_producto = EstadoProducto.objects.get(nombre = ESTADO_HABILITADO)

            if Producto.objects.filter(codigo = codigo,
                                       estado = estado_habilitado_producto).__len__() <1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_INEXISTENTE)
            else:
                producto_modificado = Producto.objects.get( codigo = codigo,
                                                            estado = estado_habilitado_producto)
                producto_modificado.nombre = nombre
                producto_modificado.marca = marca
                producto_modificado.medida = medida
                producto_modificado.unidad_medida = unidad_medida
                producto_modificado.stock_minimo = stock_minimo
                producto_modificado.save()
                response.content = armar_response_content(None, MODIFICACION_PRODUCTO)
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
def eliminar_producto(request):

    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if CODIGO in datos and not (CODIGO == ''):
                codigo = datos[CODIGO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_PRODUCTO_FALTANTE)

            estado_habilitado = EstadoProducto.objects.get(nombre = ESTADO_HABILITADO)

            if Producto.objects.filter(codigo=codigo, estado = estado_habilitado).__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_INEXISTENTE)
            else:
                estado_deshabilitado = EstadoProducto.objects.get(nombre = ESTADO_DESHABILITADO)
                producto_eliminado = Producto.objects.get(codigo=codigo, estado=estado_habilitado)
                producto_eliminado.estado = estado_deshabilitado
                producto_eliminado.save()
                response.content = armar_response_content(None, ELIMINACION_PRODUCTO)
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
def obtener_productos(request):

    try:
        response = HttpResponse()
        estado_habilitado = EstadoProducto.objects.get(nombre = ESTADO_HABILITADO)
        if Producto.objects.filter(estado = estado_habilitado).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PRODUCTOS_INEXISTENTES)
        else:
            productos = Producto.objects.filter(estado=estado_habilitado)
            response.content = armar_response_list_content(productos)
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
def obtener_producto_id(request,id_producto):

    try:
        response = HttpResponse()
        if id_producto == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_PRODUCTO_FALTANTE)
        estado_habilitado = EstadoProducto.objects.get(nombre = ESTADO_HABILITADO)
        if Producto.objects.filter(codigo = id_producto,estado = estado_habilitado).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PRODUCTO_INEXISTENTE)
        else:
            producto = Producto.objects.get(codigo = id_producto, estado=estado_habilitado)
            response.content = armar_response_content(producto)
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
def obtener_productos_categoriaid(request,id_categoria):

    try:
        response = HttpResponse()
        if id_categoria == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_CATEGORIA_FALTANTE)
        estado_habilitado_categoria = EstadoCategoria.objects.get(nombre = ESTADO_HABILITADO)
        if Categoria.objects.filter(codigo = id_categoria,estado = estado_habilitado_categoria).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CATEGORIA_INEXISTENTE)
        else:
            estado_habilitado_producto = EstadoProducto.objects.get(nombre=ESTADO_HABILITADO)
            if Producto.objects.filter(categoria = id_categoria, estado=estado_habilitado_producto).__len__()>=1:
                productos = Producto.objects.filter(categoria=id_categoria,
                                                            estado=estado_habilitado_producto)
                response.content = armar_response_list_content(productos)
                response.status_code = 200
                return response
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CATEGORIA_PRODUCTO_INEXISTENTE)
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_GET])
def obtener_productos_no_categoriaid(request,id_categoria):

    try:
        response = HttpResponse()
        if id_categoria == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_CATEGORIA_FALTANTE)
        estado_habilitado_categoria = EstadoCategoria.objects.get(nombre = ESTADO_HABILITADO)
        if Categoria.objects.filter(codigo = id_categoria,estado = estado_habilitado_categoria).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CATEGORIA_INEXISTENTE)
        else:
            estado_habilitado_producto = EstadoProducto.objects.get(nombre=ESTADO_HABILITADO)
            if Producto.objects.filter(estado=estado_habilitado_producto).exclude(categoria = id_categoria).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PRODUCTOS_INEXISTENTES)
            else:
                productos = Producto.objects.filter(estado=estado_habilitado_producto).exclude(categoria=id_categoria)
                response.content = armar_response_list_content(productos)
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
@metodos_requeridos([METODO_POST])
def asginar_producto_categoria(request):

    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()
        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        if ID_CATEGORIA in datos and not ID_CATEGORIA == '':
            id_categoria = datos[ID_CATEGORIA]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_CATEGORIA_FALTANTE)

        if ID_PRODUCTO in datos and not ID_PRODUCTO == '':
            id_producto = datos[ID_PRODUCTO]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_PRODUCTO_FALTANTE)

        estado_habilitado_categoria = EstadoCategoria.objects.get(nombre = ESTADO_HABILITADO)
        if Categoria.objects.filter(codigo = id_categoria,estado = estado_habilitado_categoria).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CATEGORIA_INEXISTENTE)
        categoria_ingresada = Categoria.objects.get(codigo = id_categoria,estado = estado_habilitado_categoria)

        estado_habilitado_producto = EstadoProducto.objects.get(nombre=ESTADO_HABILITADO)
        if Producto.objects.filter(codigo = id_producto,estado = estado_habilitado_producto).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PRODUCTO_INEXISTENTE)

        producto_ingresado = Producto.objects.get(codigo = id_producto, estado = estado_habilitado_producto)
        producto_ingresado.categoria = categoria_ingresada
        producto_ingresado.save()
        response.content = armar_response_content(None,ASIGNACION_PRODUCTO_EXITOSA)
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
def obtener_productos_subcategoriaid(request,id_subcategoria):

    try:
        response = HttpResponse()
        if id_subcategoria == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_SUBCATEGORIA_FALTANTE)
        estado_habilitado_subcategoria = EstadoSubCategoria.objects.get(nombre = ESTADO_HABILITADO)
        if SubCategoria.objects.filter(codigo = id_subcategoria,estado = estado_habilitado_subcategoria).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_SUBCATEGORIA_INEXISTENTE)
        else:
            estado_habilitado_producto = EstadoProducto.objects.get(nombre=ESTADO_HABILITADO)
            if Producto.objects.filter(subcategoria = id_subcategoria, estado=estado_habilitado_producto).__len__()>=1:
                productos = Producto.objects.filter(subcategoria=id_subcategoria,
                                                            estado=estado_habilitado_producto)
                response.content = armar_response_list_content(productos)
                response.status_code = 200
                return response
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_SUBCATEGORIA_PRODUCTO_INEXISTENTE)
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_GET])
def obtener_productos_no_subcategoriaid(request,id_subcategoria):

    try:
        response = HttpResponse()
        if id_subcategoria == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_SUBCATEGORIA_FALTANTE)
        estado_habilitado_subcategoria = EstadoSubCategoria.objects.get(nombre = ESTADO_HABILITADO)
        if SubCategoria.objects.filter(codigo = id_subcategoria,estado = estado_habilitado_subcategoria).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_SUBCATEGORIA_INEXISTENTE)
        else:
            estado_habilitado_producto = EstadoProducto.objects.get(nombre=ESTADO_HABILITADO)
            if Producto.objects.filter(estado=estado_habilitado_producto).exclude(subcategoria = id_subcategoria).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PRODUCTOS_INEXISTENTES)
            else:
                productos = Producto.objects.filter(estado=estado_habilitado_producto).exclude(subcategoria=id_subcategoria)
                response.content = armar_response_list_content(productos)
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
@metodos_requeridos([METODO_POST])
def asiginar_producto_subcategoria(request):

    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()
        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        if ID_SUBCATEGORIA in datos and not ID_SUBCATEGORIA == '':
            id_subcategoria = datos[ID_SUBCATEGORIA]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_SUBCATEGORIA_FALTANTE)

        if ID_PRODUCTO in datos and not ID_PRODUCTO == '':
            id_producto = datos[ID_PRODUCTO]
        else:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_PRODUCTO_FALTANTE)

        estado_habilitado_subcategoria = EstadoSubCategoria.objects.get(nombre = ESTADO_HABILITADO)
        if SubCategoria.objects.filter(codigo = id_subcategoria,estado = estado_habilitado_subcategoria).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_SUBCATEGORIA_INEXISTENTE)
        subcategoria_ingresada = SubCategoria.objects.get(codigo = id_subcategoria,estado = estado_habilitado_subcategoria)

        estado_habilitado_producto = EstadoProducto.objects.get(nombre=ESTADO_HABILITADO)
        if Producto.objects.filter(codigo = id_producto,estado = estado_habilitado_producto).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PRODUCTO_INEXISTENTE)

        producto_ingresado = Producto.objects.get(codigo = id_producto, estado = estado_habilitado_producto)
        producto_ingresado.subcategoria = subcategoria_ingresada
        producto_ingresado.save()
        response.content = armar_response_content(None,ASIGNACION_PRODUCTO_EXITOSA)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)
