from __future__ import unicode_literals

import datetime
from string import lower

import pytz
from django.db import transaction
from django.db import IntegrityError
from iteration_utilities import duplicates

from sistema.models import *
from sistema.utils.utils import *
from sistema.utils.constantes import *
from sistema.utils.decorators import *
from sistema.utils.dto import  *
from sistema.utils.error_handler import *


@transaction.atomic()
@metodos_requeridos([METODO_POST])
def registrar_remito(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if ID_USUARIO in datos and not (ID_USUARIO == ''):
                id_usuario = datos[ID_USUARIO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_ID_USUARIO_FALTANTE)

            if Usuario.objects.filter(id = id_usuario).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_USUARIO_INEXISTENTE)

            usuario = Usuario.objects.get(id = id_usuario)

            if LISTA_PRODUCTOS in datos and not (LISTA_PRODUCTOS == []):
                lista_productos = datos[LISTA_PRODUCTOS]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRODUCTO_COMBO_FALTANTE) #es un msj de error generico

            if list(duplicates(lista_productos)):
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRODUCTO_COMBO_PRODUCTOS_REPETIDOS)

            if CANTIDAD_PRODUCTOS in datos and not (CANTIDAD_PRODUCTOS == []):
                cantidad_productos = datos[CANTIDAD_PRODUCTOS]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CANTIDAD_PRODUCTO_COMBO_FALTANTE)
            for x in range(0, cantidad_productos.__len__()):
                if cantidad_productos[x] <= 0:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CANTIDAD_PRODUCTO_COMBO_MENOR)

            if (cantidad_productos.__len__() != lista_productos.__len__()):
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CANTIDAD_LISTA_PRODUCTO_COMPRA_LONGITUD_DISTINTA)


            estado_creado = EstadoMovimientoStock.objects.get(nombre = ESTADO_CREADO)
            tipo_movimiento_stock = TipoMovimientoStock.objects.get(nombre = MOVIMIENTO_REMITO)

            movimiento_stock_remito = MovimientoStock(fecha_creacion = datetime.datetime.now(pytz.utc),
                                                      usuario = usuario,
                                                      tipo_movimiento = tipo_movimiento_stock,
                                                      estado = estado_creado)
            movimiento_stock_remito.saveNewMovimientoStock()

            for x in range(lista_productos.__len__()):
                if Producto.objects.filter(codigo = lista_productos[x]).__len__()<1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_PRODUCTO_INEXISTENTE)

                producto_actual = Producto.objects.get(codigo = lista_productos[x])

                if producto_actual.stock_deposito < cantidad_productos[x]:
                    raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_CANTIDAD_NO_DISPONIBLE)

                movimiento_stock_detalle = MovimientoStockDetalle(cantidad = cantidad_productos[x] ,
                                                                  movimiento_stock= movimiento_stock_remito,
                                                                  producto= producto_actual)
                movimiento_stock_detalle.save()
                producto_actual.stock_deposito -= cantidad_productos[x]
                producto_actual.stock_local += cantidad_productos[x]
                producto_actual.save()

            movimiento_stock_remito.save()
            response.content = armar_response_content(None, CREACION_REMITO)
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
def cancelar_remito(request,id_remito):
    try:
        response = HttpResponse()

        if id_remito == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:

            estado_creado_remito = EstadoMovimientoStock.objects.get(nombre = ESTADO_CREADO)
            tipo_movimiento_stock = TipoMovimientoStock.objects.get(nombre = MOVIMIENTO_REMITO)

            if MovimientoStock.objects.filter(codigo = id_remito, estado = estado_creado_remito, tipo_movimiento= tipo_movimiento_stock).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_REMITO_INEXISTENTE)

            movimiento_remito = MovimientoStock.objects.get(codigo = id_remito, estado = estado_creado_remito, tipo_movimiento= tipo_movimiento_stock)

            if MovimientoStockDetalle.objects.filter(movimiento_stock = movimiento_remito).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REMITO_SIN_DETALLE)

            movimiento_detalle_remito = MovimientoStockDetalle.objects.filter(movimiento_stock = movimiento_remito)

            for x in range(movimiento_detalle_remito.__len__()):
                codigo_producto_detalle_remito = movimiento_detalle_remito[x].producto.codigo

                if Producto.objects.filter(codigo = codigo_producto_detalle_remito).__len__()<1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_PRODUCTO_INEXISTENTE)

                producto = Producto.objects.get(codigo = codigo_producto_detalle_remito)
                producto.stock_deposito += movimiento_detalle_remito[x].cantidad
                producto.stock_local -= movimiento_detalle_remito[x].cantidad
                producto.save()

            estado_cancelado_remito = EstadoMovimientoStock.objects.get(nombre = ESTADO_CANCELADO)
            movimiento_remito.estado = estado_cancelado_remito
            movimiento_remito.save()
            response.content = armar_response_content(None, CANCELACION_REMITO)
            response.status_code = 200
            return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)