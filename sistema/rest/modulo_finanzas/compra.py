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
def registrar_compra(request):
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

            if DESCUENTO in datos and not DESCUENTO == '' and datos[DESCUENTO] >0:
                descuento = datos[DESCUENTO]
            else:
                descuento = None

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

            estado_lista_precio_habilitado = EstadoListaPrecio.objects.get(nombre= ESTADO_HABILITADO)

            if ListaPrecio.objects.filter(estado = estado_lista_precio_habilitado).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_LISTA_PRECIO_NO_HABILITADA)

            lista_precio = ListaPrecio.objects.get(estado = estado_lista_precio_habilitado)

            estado_creado = EstadoMovimientoStock.objects.get(nombre = ESTADO_CREADO)
            tipo_movimiento_stock = TipoMovimientoStock.objects.get(nombre = MOVIMIENTO_COMPRA)

            movimiento_stock_compra = MovimientoStock(fecha_creacion = datetime.datetime.now(pytz.utc),
                                                      total_parcial = 0,
                                                      total_final = 0,
                                                      descuento = descuento,
                                                      usuario = usuario,
                                                      tipo_movimiento = tipo_movimiento_stock,
                                                      estado = estado_creado)
            movimiento_stock_compra.saveNewMovimientoStock()

            for x in range(lista_productos.__len__()):
                if Producto.objects.filter(codigo = lista_productos[x]).__len__()<1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_PRODUCTO_INEXISTENTE)

                producto_actual = Producto.objects.get(codigo = lista_productos[x])

                if ListaPrecioDetalle.objects.filter(lista_precio = lista_precio, producto=producto_actual).__len__()<1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_PRODUCTO_INEXISTENTE_LISTA)

                detalle_lista_precio = ListaPrecioDetalle.objects.get(lista_precio = lista_precio , producto = producto_actual)

                movimiento_stock_detalle = MovimientoStockDetalle(cantidad = cantidad_productos[x] ,
                                                                  precio_unitario = detalle_lista_precio.precio_unitario_compra,
                                                                  subtotal = detalle_lista_precio.precio_unitario_compra * cantidad_productos[x],
                                                                  movimiento_stock= movimiento_stock_compra,
                                                                  producto= producto_actual)
                movimiento_stock_detalle.save()
                movimiento_stock_compra.total_parcial += movimiento_stock_detalle.cantidad * movimiento_stock_detalle.precio_unitario

                producto_actual.stock_deposito = producto_actual.stock_deposito + cantidad_productos[x]
                producto_actual.save()

            #aplicamos el descuento si corresponde
            if descuento is not None:
                movimiento_stock_compra.total_final = movimiento_stock_compra.total_parcial - (movimiento_stock_compra.total_parcial * descuento)
            else:
                movimiento_stock_compra.total_final = movimiento_stock_compra.total_parcial
            movimiento_stock_compra.save()
            response.content = armar_response_content(None, CREACION_COMPRA)
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
def cancelar_compra(request,id_compra):
    try:
        response = HttpResponse()

        if id_compra == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:

            estado_creado_compra = EstadoMovimientoStock.objects.get(nombre = ESTADO_CREADO)
            tipo_movimiento_stock = TipoMovimientoStock.objects.get(nombre = MOVIMIENTO_COMPRA)

            if MovimientoStock.objects.filter(codigo = id_compra, estado = estado_creado_compra, tipo_movimiento= tipo_movimiento_stock).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_COMPRA_INEXISTENTE)

            movimiento_compra = MovimientoStock.objects.get(codigo = id_compra, estado = estado_creado_compra, tipo_movimiento= tipo_movimiento_stock)

            if MovimientoStockDetalle.objects.filter(movimiento_stock = movimiento_compra).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_COMPRA_SIN_DETALLE)

            movimiento_detalle_compra = MovimientoStockDetalle.objects.filter(movimiento_stock = movimiento_compra)

            for x in range(movimiento_detalle_compra.__len__()):
                codigo_producto_detalle_compra = movimiento_detalle_compra[x].producto.codigo

                if Producto.objects.filter(codigo = codigo_producto_detalle_compra).__len__()<1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_PRODUCTO_INEXISTENTE)

                producto = Producto.objects.get(codigo = codigo_producto_detalle_compra)
                producto.stock_deposito = producto.stock_deposito - movimiento_detalle_compra[x].cantidad
                producto.save()

            estado_cancelado_compra = EstadoMovimientoStock.objects.get(nombre = ESTADO_CANCELADO)
            movimiento_compra.estado = estado_cancelado_compra
            movimiento_compra.save()
            response.content = armar_response_content(None, CANCELACION_COMPRA)
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
def pagar_compra(request,id_compra):
    try:
        response = HttpResponse()

        if id_compra == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:

            estado_creado_compra = EstadoMovimientoStock.objects.get(nombre = ESTADO_CREADO)
            tipo_movimiento_stock = TipoMovimientoStock.objects.get(nombre = MOVIMIENTO_COMPRA)

            if MovimientoStock.objects.filter(codigo = id_compra, estado = estado_creado_compra, tipo_movimiento= tipo_movimiento_stock).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_COMPRA_INEXISTENTE)

            movimiento_compra = MovimientoStock.objects.get(codigo = id_compra, estado = estado_creado_compra, tipo_movimiento= tipo_movimiento_stock)

            estado_pagado_compra = EstadoMovimientoStock.objects.get(nombre = ESTADO_PAGADO)
            movimiento_compra.estado = estado_pagado_compra
            movimiento_compra.save()
            response.content = armar_response_content(None, PAGO_COMPRA)
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
def generar_movimiento_capital_compra_movimiento_stock(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if CODIGO in datos and not (CODIGO == ''):
                id_compra = datos[CODIGO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_COMPRA_FALTANTE)

            salida_movimiento_capital = TipoMovimientoCapital.objects.get(nombre = MOVIMIENTO_SALIDA_CAPITAL)

            estado_compra_pagado = EstadoMovimientoStock.objects.get(nombre = ESTADO_PAGADO)

            if MovimientoStock.objects.filter(codigo = id_compra, estado = estado_compra_pagado).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_COMPRA_INEXISTENTE)

            movimiento_compra = MovimientoStock.objects.get(codigo = id_compra, estado = estado_compra_pagado)

            estado_movimiento_capital_pagado = EstadoMovimientoCapital.objects.get(nombre = ESTADO_PAGADO)

            forma_pago = FormaPago.objects.get(nombre = FORMA_PAGO_EFECTIVO) #Por defecto la forma de pago siempre es efectivo

            movimiento_capital_salida = MovimientoCapital(total = movimiento_compra.total_final,
                                                          fecha_creacion = datetime.datetime.now(pytz.utc),
                                                          descripcion_movimiento = (PAGO_MOVIMIENTO_CAPITAL.append(str(movimiento_compra.codigo))),
                                                          tipo_movimiento = salida_movimiento_capital,
                                                          estado = estado_movimiento_capital_pagado,
                                                          movimiento_stock = movimiento_compra,
                                                          forma_pago = forma_pago
                                                          )
            movimiento_capital_salida.saveNewMovimientoCapital()
            response.content = armar_response_content(None, CREACION_MOVIMIENTO_CAPITAL_SALIDA)
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
def generar_movimiento_capital_compra(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if DESCRIPCION in datos and not (DESCRIPCION == ''):
                descripcion = datos[DESCRIPCION]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DESCRIPCION_MOVIMIENTO_CAPITAL_SALIDA_FALTANTE)

            if TOTAL in datos and not (TOTAL == ''):
                total = datos[TOTAL]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_TOTAL_MOVIMIENTO_CAPITAL_SALIDA_FALTANTE)

            if total <= 0:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_TOTAL_MOVIMIENTO_CAPITAL_SALIDA_INSUFICIENTE)

            salida_movimiento_capital = TipoMovimientoCapital.objects.get(nombre = MOVIMIENTO_SALIDA_CAPITAL)

            estado_movimiento_capital_pagado = EstadoMovimientoCapital.objects.get(nombre = ESTADO_PAGADO)

            forma_pago = FormaPago.objects.get(nombre = FORMA_PAGO_EFECTIVO) #Por defecto la forma de pago siempre es efectivo

            movimiento_capital_salida = MovimientoCapital(total = total,
                                                          fecha_creacion = datetime.datetime.now(pytz.utc),
                                                          descripcion_movimiento = descripcion,
                                                          tipo_movimiento = salida_movimiento_capital,
                                                          estado = estado_movimiento_capital_pagado,
                                                          movimiento_stock = None,
                                                          forma_pago = forma_pago
                                                          )
            movimiento_capital_salida.saveNewMovimientoCapital()
            response.content = armar_response_content(None, CREACION_MOVIMIENTO_CAPITAL_SALIDA)
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
def cancelar_movimiento_capital_compra(request,id_movimiento_salida):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if id_movimiento_salida == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_MOVIMIENTO_CAPITAL_SALIDA_FALTANTE)
        else:
            estado_movimiento_capital_pagado = EstadoMovimientoCapital.objects.get(nombre=ESTADO_PAGADO)

            if MovimientoCapital.objects.filter(codigo=id_movimiento_salida,
                                                estado=estado_movimiento_capital_pagado,
                                                movimiento_stock=None).__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_MOVIMIENTO_SALIDA_CAPITAL_INEXISTENTE)

            movimiento_capital = MovimientoCapital.objects.get(codigo=id_movimiento_salida, estado=estado_movimiento_capital_pagado)

            estado_movimiento_capital_cancelado = EstadoMovimientoCapital.objects.get(nombre=ESTADO_CANCELADO)

            movimiento_capital.estado = estado_movimiento_capital_cancelado
            movimiento_capital.save()
            response.content = armar_response_content(None, CANCELACION_MOVIMIENTO_CAPITAL_SALIDA)
            response.status_code = 200
            return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)