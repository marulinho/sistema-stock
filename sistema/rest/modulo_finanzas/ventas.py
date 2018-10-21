from __future__ import unicode_literals

import datetime

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
def registrar_venta(request):
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

            if ID_CLIENTE in datos and not (datos[ID_CLIENTE]==''):
                id_cliente = datos[ID_CLIENTE]

                if Cliente.objects.filter(codigo = id_cliente).__len__()<1:
                   raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_ID_CLIENTE_FALTANTE)

                cliente  = Cliente.objects.get(codigo = id_cliente)

            else:
                cliente = None

            if MEDIO_PAGO in datos and not (datos[MEDIO_PAGO] == ''):
                medio_pago = datos[MEDIO_PAGO]

                if FormaPago.objects.filter(nombre=medio_pago).__len__()<1:
                    raise ValueError (ERROR_DATOS_INCORRECTOS,DETALLE_FORMA_PAGO_FALTANTE)
                else:
                    forma_pago = FormaPago.objects.get(nombre=medio_pago)
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_FORMA_PAGO_FALTANTE)

            if DESCUENTO in datos and not DESCUENTO == '' and datos[DESCUENTO] >=0:
                descuento = datos[DESCUENTO]
            else:
                descuento = None

            if LISTA_PRODUCTOS in datos and (not datos[LISTA_PRODUCTOS] == []):
                lista_productos = datos[LISTA_PRODUCTOS]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRODUCTO_COMBO_FALTANTE) #es un msj de error generico

            if CANTIDAD_PRODUCTOS in datos and (not datos[CANTIDAD_PRODUCTOS] == []):
                cantidad_productos = datos[CANTIDAD_PRODUCTOS]

            for x in range(0, cantidad_productos.__len__()):
                if cantidad_productos[x] <= 0:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CANTIDAD_PRODUCTO_COMBO_MENOR)

            if list(duplicates(lista_productos)):
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_PRODUCTO_COMBO_PRODUCTOS_REPETIDOS)

            if LISTA_COMBOS in datos and (not datos[LISTA_COMBOS] == []):
                lista_combos = datos[LISTA_COMBOS]
            else:
                lista_combos=[]

            if list(duplicates(lista_combos)):
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_COMBO_REPETIDOS)

            if CANTIDAD_PRODUCTOS_COMBO in datos and (not datos[CANTIDAD_PRODUCTOS_COMBO] == []):
                cantidad_productos_combo = datos[CANTIDAD_PRODUCTOS_COMBO]
            else:
                cantidad_productos_combo = []

            if (CANTIDAD_PRODUCTOS_COMBO not in datos or (datos[CANTIDAD_PRODUCTOS_COMBO] == [])) and (CANTIDAD_PRODUCTOS not in datos or(datos[CANTIDAD_PRODUCTOS] == [])):
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CANTIDAD_PRODUCTO_COMBO_FALTANTE)

            for x in range(0, cantidad_productos_combo.__len__()):
                if cantidad_productos_combo[x] <= 0:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CANTIDAD_PRODUCTO_COMBO_MENOR)

            if (cantidad_productos.__len__() != lista_productos.__len__()):
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CANTIDAD_LISTA_PRODUCTO_COMPRA_LONGITUD_DISTINTA)

            estado_lista_precio_habilitado = EstadoListaPrecio.objects.get(nombre= ESTADO_HABILITADO)

            if ListaPrecio.objects.filter(estado = estado_lista_precio_habilitado).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_LISTA_PRECIO_NO_HABILITADA)

            lista_precio = ListaPrecio.objects.get(estado = estado_lista_precio_habilitado)

            estado_creado = EstadoMovimientoStock.objects.get(nombre = ESTADO_CREADO)
            tipo_movimiento_stock = TipoMovimientoStock.objects.get(nombre = MOVIMIENTO_VENTA)

            if medio_pago == FORMA_PAGO_CUENTA_CORRIENTE and cliente is None:
                raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_ID_CLIENTE_FALTANTE)

            if cliente is None:

                movimiento_stock_venta = MovimientoStock(fecha_creacion = datetime.datetime.now(pytz.utc),
                                                      total_parcial = 0,
                                                      total_final = 0,
                                                      descuento = descuento,
                                                      usuario = usuario,
                                                      tipo_movimiento = tipo_movimiento_stock,
                                                      estado = estado_creado,
                                                      cliente = None,
                                                      forma_pago = forma_pago)
            else:
                movimiento_stock_venta = MovimientoStock(fecha_creacion=datetime.datetime.now(pytz.utc),
                                                         total_parcial=0,
                                                         total_final=0,
                                                         descuento=descuento,
                                                         usuario=usuario,
                                                         tipo_movimiento=tipo_movimiento_stock,
                                                         estado=estado_creado,
                                                         cliente=cliente,
                                                         forma_pago=forma_pago)
            movimiento_stock_venta.saveNewMovimientoStock()

            for x in range(lista_productos.__len__()):
                if Producto.objects.filter(codigo = lista_productos[x]).__len__()<1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_PRODUCTO_INEXISTENTE)

                producto_actual = Producto.objects.get(codigo = lista_productos[x])

                if producto_actual.stock_local < cantidad_productos[x]:
                    raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_STOCK_INSUFICIENTE_VENTA)

                if ListaPrecioDetalle.objects.filter(lista_precio = lista_precio, producto=producto_actual).__len__()<1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_PRODUCTO_INEXISTENTE_LISTA)

                detalle_lista_precio = ListaPrecioDetalle.objects.get(lista_precio = lista_precio , producto = producto_actual)

                movimiento_stock_detalle = MovimientoStockDetalle(cantidad = cantidad_productos[x] ,
                                                                  precio_unitario = detalle_lista_precio.precio_unitario_venta,
                                                                  precio_compra = detalle_lista_precio.precio_unitario_compra,
                                                                  subtotal = detalle_lista_precio.precio_unitario_venta * cantidad_productos[x],
                                                                  movimiento_stock= movimiento_stock_venta,
                                                                  producto= producto_actual,
                                                                  combo = None)
                movimiento_stock_detalle.save()
                movimiento_stock_venta.total_parcial += movimiento_stock_detalle.subtotal

                producto_actual.stock_local -= cantidad_productos[x]
                producto_actual.save()

            for x in range(0,lista_combos.__len__()):
                if Combo.objects.filter(codigo = lista_combos[x]).__len__()<1:
                    raise ValueError(DETALLE_ERROR_DATOS_INCOMPLETOS,DETALLE_ERROR_CODIGO_COMBO_INEXISTENTE)

                combo = Combo.objects.get(codigo = lista_combos[x])
                movimiento_stock_detalle = MovimientoStockDetalle(cantidad=cantidad_productos_combo[x],
                                                                  precio_unitario=combo.precio,
                                                                  precio_compra=None,
                                                                  subtotal=combo.precio * cantidad_productos_combo[x],
                                                                  movimiento_stock=movimiento_stock_venta,
                                                                  producto=None,
                                                                  combo = combo)
                movimiento_stock_detalle.save()

                if ComboDetalle.objects.filter(combo = combo).__len__()<1:
                    raise ValueError(DETALLE_ERROR_DATOS_INCOMPLETOS, DETALLE_ERROR_COMBO_SIN_DETALLE)

                detalle_combo = ComboDetalle.objects.filter(combo = combo)

                for y in range(0,detalle_combo.__len__()):
                    producto_actual = Producto.objects.get(codigo=detalle_combo[y].producto.codigo)

                    if producto_actual.stock_local < detalle_combo[y].cantidad * cantidad_productos_combo[x]:
                        raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_STOCK_INSUFICIENTE_VENTA)

                    movimiento_stock_venta.save()
                    movimiento_stock_venta.total_parcial += detalle_combo[y].subtotal * cantidad_productos_combo[x]

                    producto_actual.stock_local -= cantidad_productos_combo[x]
                    producto_actual.save()

            #aplicamos el descuento si corresponde
            if descuento is not None:
                movimiento_stock_venta.total_final = movimiento_stock_venta.total_parcial - (movimiento_stock_venta.total_parcial * descuento / 100)
            else:
                movimiento_stock_venta.total_final = movimiento_stock_venta.total_parcial
            movimiento_stock_venta.save()

            if cliente is None:
                dto_venta = DTOCabeceraMovimientoStock(movimiento_stock_venta.codigo,
                                                      parsear_fecha_a_hora_arg(movimiento_stock_venta.fecha_creacion),
                                                      movimiento_stock_venta.total_parcial,
                                                      movimiento_stock_venta.descuento,
                                                      movimiento_stock_venta.total_final,
                                                      movimiento_stock_venta.usuario.nombre,
                                                      movimiento_stock_venta.estado.nombre,
                                                      movimiento_stock_venta.tipo_movimiento.nombre,
                                                      None)
            else:
                dto_venta = DTOCabeceraMovimientoStock(movimiento_stock_venta.codigo,
                                                       parsear_fecha_a_hora_arg(movimiento_stock_venta.fecha_creacion),
                                                       movimiento_stock_venta.total_parcial,
                                                       movimiento_stock_venta.descuento,
                                                       movimiento_stock_venta.total_final,
                                                       movimiento_stock_venta.usuario.nombre,
                                                       movimiento_stock_venta.estado.nombre,
                                                       movimiento_stock_venta.tipo_movimiento.nombre,
                                                       movimiento_stock_venta.cliente.nombre +' '+movimiento_stock_venta.cliente.apellido)

            response.content = armar_response_content(dto_venta)
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
def cancelar_venta(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if CODIGO not in datos or CODIGO == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            id_venta = datos[CODIGO]

            estado_cancelado_venta = EstadoMovimientoStock.objects.get(nombre = ESTADO_CANCELADO)
            tipo_movimiento_stock = TipoMovimientoStock.objects.get(nombre = MOVIMIENTO_VENTA)

            if MovimientoStock.objects.filter(codigo = id_venta, estado = estado_cancelado_venta, tipo_movimiento= tipo_movimiento_stock).__len__()>=1:
                raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_VENTA_CANCELADA)

            movimiento_venta = MovimientoStock.objects.get(codigo = id_venta, tipo_movimiento= tipo_movimiento_stock)

            if MovimientoStockDetalle.objects.filter(movimiento_stock = movimiento_venta).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_VENTA_SIN_DETALLE)

            movimiento_detalle_venta = MovimientoStockDetalle.objects.filter(movimiento_stock = movimiento_venta)

            for x in range(movimiento_detalle_venta.__len__()):
                codigo_producto_detalle_venta = movimiento_detalle_venta[x].producto.codigo

                if Producto.objects.filter(codigo = codigo_producto_detalle_venta).__len__()<1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_PRODUCTO_INEXISTENTE)

                producto = Producto.objects.get(codigo = codigo_producto_detalle_venta)

                producto.stock_local = producto.stock_local + movimiento_detalle_venta[x].cantidad
                producto.save()

            estado_venta = movimiento_venta.estado
            estado_pagado = EstadoMovimientoStock.objects.get(nombre = ESTADO_PAGADO)

            if estado_venta == estado_pagado:
                tipo_movimiento_capital = TipoMovimientoCapital.objects.get(nombre = MOVIMIENTO_ENTRADA_CAPITAL)
                if MovimientoCapital.objects.filter(tipo_movimiento = tipo_movimiento_capital, movimiento_stock = movimiento_venta).__len__()<1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_VENTA_SIN_MOVIMIENTO_CAPITAL)

                movimiento_entrada_capital = MovimientoCapital.objects.filter(tipo_movimiento = tipo_movimiento_capital, movimiento_stock = movimiento_venta)
                estado_cancelado_movimiento_capital = EstadoMovimientoCapital.objects.get(nombre = ESTADO_CANCELADO)
                movimiento_entrada_capital.estado = estado_cancelado_movimiento_capital
                movimiento_entrada_capital.save()
            movimiento_venta.estado = estado_cancelado_venta
            movimiento_venta.save()
            if movimiento_venta.cliente is None:
                dto_venta = DTOCabeceraMovimientoStock(movimiento_venta.codigo,
                                                   parsear_fecha_a_hora_arg(movimiento_venta.fecha_creacion),
                                                   movimiento_venta.total_parcial,
                                                   movimiento_venta.descuento,
                                                   movimiento_venta.total_final,
                                                   movimiento_venta.usuario.nombre,
                                                   movimiento_venta.estado.nombre,
                                                   movimiento_venta.tipo_movimiento.nombre)
            else:
                dto_venta = DTOCabeceraMovimientoStock(movimiento_venta.codigo,
                                                       parsear_fecha_a_hora_arg(movimiento_venta.fecha_creacion),
                                                       movimiento_venta.total_parcial,
                                                       movimiento_venta.descuento,
                                                       movimiento_venta.total_final,
                                                       movimiento_venta.usuario.nombre,
                                                       movimiento_venta.estado.nombre,
                                                       movimiento_venta.tipo_movimiento.nombre,
                                                       movimiento_venta.cliente.nombre +' '+movimiento_venta.cliente.apellido)
            response.content = armar_response_content(dto_venta)
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
def cobrar_venta(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if CODIGO not in datos or CODIGO == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            id_venta = datos[CODIGO]

            estado_creado_venta = EstadoMovimientoStock.objects.get(nombre = ESTADO_CREADO)
            tipo_movimiento_stock = TipoMovimientoStock.objects.get(nombre = MOVIMIENTO_VENTA)

            if MovimientoStock.objects.filter(codigo = id_venta, estado = estado_creado_venta, tipo_movimiento= tipo_movimiento_stock).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_VENTA_INEXISTENTE)

            movimiento_venta = MovimientoStock.objects.get(codigo = id_venta, estado = estado_creado_venta, tipo_movimiento= tipo_movimiento_stock)

            estado_pagado_venta = EstadoMovimientoStock.objects.get(nombre = ESTADO_PAGADO)
            movimiento_venta.estado = estado_pagado_venta
            movimiento_venta.save()
            if movimiento_venta.cliente is None:
                dto_venta = DTOCabeceraMovimientoStock(movimiento_venta.codigo,
                                                   parsear_fecha_a_hora_arg(movimiento_venta.fecha_creacion),
                                                   movimiento_venta.total_parcial,
                                                   movimiento_venta.descuento,
                                                   movimiento_venta.total_final,
                                                   movimiento_venta.usuario.nombre,
                                                   movimiento_venta.estado.nombre,
                                                   movimiento_venta.tipo_movimiento.nombre)
            else:
                dto_venta = DTOCabeceraMovimientoStock(movimiento_venta.codigo,
                                                       parsear_fecha_a_hora_arg(movimiento_venta.fecha_creacion),
                                                       movimiento_venta.total_parcial,
                                                       movimiento_venta.descuento,
                                                       movimiento_venta.total_final,
                                                       movimiento_venta.usuario.nombre,
                                                       movimiento_venta.estado.nombre,
                                                       movimiento_venta.tipo_movimiento.nombre,
                                                       movimiento_venta.cliente.nombre +' '+movimiento_venta.cliente.apellido)
            response.content = armar_response_content(dto_venta)
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
def cambiar_estado_venta(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if ESTADO not in datos or ESTADO == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            estado = datos[ESTADO]

        if CODIGO not in datos or CODIGO == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            codigo = datos[CODIGO]

            if EstadoMovimientoStock.objects.filter(nombre = estado).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_ESTADO_INEXISTENTE)

            estado_venta = EstadoMovimientoStock.objects.get(nombre = estado)

            tipo_movimiento_stock = TipoMovimientoStock.objects.get(nombre = MOVIMIENTO_VENTA)

            if MovimientoStock.objects.filter(codigo = codigo, tipo_movimiento= tipo_movimiento_stock).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_COMPRA_INEXISTENTE)

            movimiento_venta = MovimientoStock.objects.get(codigo = codigo, tipo_movimiento= tipo_movimiento_stock)

            movimiento_venta.estado = estado_venta
            movimiento_venta.save()

            if movimiento_venta.cliente is None:
                dto_venta = DTOCabeceraMovimientoStock(movimiento_venta.codigo,
                                                   parsear_fecha_a_hora_arg(movimiento_venta.fecha_creacion),
                                                   movimiento_venta.total_parcial,
                                                   movimiento_venta.descuento,
                                                   movimiento_venta.total_final,
                                                   movimiento_venta.usuario.nombre,
                                                   movimiento_venta.estado.nombre,
                                                   movimiento_venta.tipo_movimiento.nombre)
            else:
                dto_venta = DTOCabeceraMovimientoStock(movimiento_venta.codigo,
                                                       parsear_fecha_a_hora_arg(movimiento_venta.fecha_creacion),
                                                       movimiento_venta.total_parcial,
                                                       movimiento_venta.descuento,
                                                       movimiento_venta.total_final,
                                                       movimiento_venta.usuario.nombre,
                                                       movimiento_venta.estado.nombre,
                                                       movimiento_venta.tipo_movimiento.nombre,
                                                       movimiento_venta.cliente.nombre +' '+movimiento_venta.cliente.apellido)
            response.content = armar_response_content(dto_venta)
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
def generar_movimiento_capital_venta_movimiento_stock(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if CODIGO in datos and not (CODIGO == ''):
                id_venta = datos[CODIGO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_VENTA_FALTANTE)

            entrada_movimiento_capital = TipoMovimientoCapital.objects.get(nombre = MOVIMIENTO_ENTRADA_CAPITAL)

            estado_venta_pagado = EstadoMovimientoStock.objects.get(nombre = ESTADO_PAGADO)

            if MovimientoStock.objects.filter(codigo = id_venta, estado = estado_venta_pagado).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_VENTA_INEXISTENTE)

            movimiento_venta = MovimientoStock.objects.get(codigo = id_venta, estado = estado_venta_pagado)

            estado_movimiento_capital_pagado = EstadoMovimientoCapital.objects.get(nombre = ESTADO_PAGADO)

            forma_pago = FormaPago.objects.get(nombre = FORMA_PAGO_EFECTIVO) #Por defecto la forma de pago siempre es efectivo

            if MovimientoCapital.objects.filter(movimiento_stock = movimiento_venta ,tipo_movimiento = entrada_movimiento_capital).__len__()>=1:
                raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_MOVIMIENTO_CAPITAL_EXISTENTE)

            movimiento_capital_entrada = MovimientoCapital(total = movimiento_venta.total_final,
                                                          fecha_creacion = datetime.datetime.now(pytz.utc),
                                                          descripcion_movimiento = (COBRO_MOVIMIENTO_CAPITAL + (str(movimiento_venta.codigo))),
                                                          tipo_movimiento = entrada_movimiento_capital,
                                                          estado = estado_movimiento_capital_pagado,
                                                          movimiento_stock = movimiento_venta,
                                                          forma_pago = forma_pago
                                                          )

            movimiento_capital_entrada.saveNewMovimientoCapital()
            dto_movimiento_capital = DTOMovimientoCapital(movimiento_capital_entrada.codigo,
                                                          movimiento_capital_entrada.total,
                                                          parsear_fecha_a_hora_arg(movimiento_capital_entrada.fecha_creacion),
                                                          movimiento_capital_entrada.descripcion_movimiento,
                                                          movimiento_capital_entrada.tipo_movimiento.nombre,
                                                          movimiento_capital_entrada.estado.nombre,
                                                          movimiento_capital_entrada.movimiento_stock.codigo,
                                                          movimiento_capital_entrada.forma_pago.nombre,
                                                          movimiento_capital_entrada.usuario)
            response.content = armar_response_content(dto_movimiento_capital)
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
def obtener_ventas(request):
    try:
        response = HttpResponse()

        tipo_movimiento_venta = TipoMovimientoStock.objects.get(nombre = MOVIMIENTO_VENTA)

        if MovimientoStock.objects.filter(tipo_movimiento = tipo_movimiento_venta).__len__()<1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_VENTAS_INEXISTENTES)

        ventas = MovimientoStock.objects.filter(tipo_movimiento = tipo_movimiento_venta).order_by('-codigo')
        lista_ventas = []
        for x in range(0,ventas.__len__()):
            if ventas[x].cliente is None:
                dto_venta = DTOCabeceraMovimientoStock(ventas[x].codigo,
                                                       parsear_fecha_a_hora_arg(ventas[x].fecha_creacion),
                                                       ventas[x].total_parcial,
                                                       ventas[x].descuento,
                                                       ventas[x].total_final,
                                                       ventas[x].usuario.nombre,
                                                       ventas[x].estado.nombre,
                                                       ventas[x].tipo_movimiento.nombre)
            else:
                dto_venta = DTOCabeceraMovimientoStock(ventas[x].codigo,
                                                       parsear_fecha_a_hora_arg(ventas[x].fecha_creacion),
                                                       ventas[x].total_parcial,
                                                       ventas[x].descuento,
                                                       ventas[x].total_final,
                                                       ventas[x].usuario.nombre,
                                                       ventas[x].estado.nombre,
                                                       ventas[x].tipo_movimiento.nombre,
                                                       ventas[x].cliente.nombre + ' ' + ventas[x].cliente.apellido)
            lista_ventas.append(dto_venta)

        response.content = armar_response_list_content(lista_ventas)
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
def obtener_venta_id(request,id_venta):
    try:
        response = HttpResponse()
        if id_venta == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_CODIGO_VENTA_FALTANTE)

        tipo_movimiento_venta = TipoMovimientoStock.objects.get(nombre=MOVIMIENTO_VENTA)

        if MovimientoStock.objects.filter(codigo = id_venta, tipo_movimiento=tipo_movimiento_venta).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_VENTA_INEXISTENTE)

        venta = MovimientoStock.objects.get(codigo = id_venta,tipo_movimiento=tipo_movimiento_venta)

        if MovimientoStockDetalle.objects.filter(movimiento_stock = venta).__len__()<1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_VENTA_SIN_DETALLE)

        movimiento_detalle_venta = MovimientoStockDetalle.objects.filter(movimiento_stock = venta)

        dto_venta = []
        dto_detalles_venta = []

        if  venta.cliente is None:
            dto_cabecera_venta = DTOCabeceraMovimientoStock(venta.codigo,
                                                        parsear_fecha_a_hora_arg(venta.fecha_creacion),
                                                        venta.total_parcial,
                                                        venta.descuento,
                                                        venta.total_final,
                                                        venta.usuario.nombre,
                                                        venta.estado.nombre,
                                                        venta.tipo_movimiento.nombre)
        else:
            dto_cabecera_venta = DTOCabeceraMovimientoStock(venta.codigo,
                                                            parsear_fecha_a_hora_arg(venta.fecha_creacion),
                                                            venta.total_parcial,
                                                            venta.descuento,
                                                            venta.total_final,
                                                            venta.usuario.nombre,
                                                            venta.estado.nombre,
                                                            venta.tipo_movimiento.nombre,
                                                            venta.cliente.nombre + ' ' + venta.cliente.apellido)

        for x in range(movimiento_detalle_venta.__len__()):

            if movimiento_detalle_venta[x].producto is not None:
                if Producto.objects.filter(codigo=movimiento_detalle_venta[x].producto.codigo).__len__() < 1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PRODUCTO_INEXISTENTE)

                producto = Producto.objects.get(codigo=movimiento_detalle_venta[x].producto.codigo)

                dto_detalle_venta = DTOMovimientoStockDetalle(producto.codigo,
                                                               producto.nombre,
                                                               producto.marca,
                                                               producto.unidad_medida.nombre,
                                                               producto.medida,
                                                               movimiento_detalle_venta[x].precio_unitario,
                                                               movimiento_detalle_venta[x].subtotal,
                                                               movimiento_detalle_venta[x].cantidad)
            else:
                #se trata de un combo
                dto_detalle_venta = DTOMovimientoStockDetalle(movimiento_detalle_venta[x].combo.codigo,
                                                              movimiento_detalle_venta[x].combo.nombre,
                                                              None,
                                                              None,
                                                              None,
                                                              movimiento_detalle_venta[x].precio_unitario,
                                                              movimiento_detalle_venta[x].subtotal,
                                                              movimiento_detalle_venta[x].cantidad)
            dto_detalles_venta.append(dto_detalle_venta)
        dto_venta = DTOListaMovimientoStock(dto_cabecera_venta,dto_detalles_venta)
        response.content = armar_response_content(dto_venta)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)