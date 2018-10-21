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
def obtener_reporte_stock_minimo(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if CANTIDAD_PRODUCTOS in datos and not (CANTIDAD_PRODUCTOS == ''):
                cantidad = datos[CANTIDAD_PRODUCTOS]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CANTIDAD_PRODUCTO_FALTANTE)

            producto_habilitado = EstadoProducto.objects.get(nombre = ESTADO_HABILITADO)

            if Producto.objects.filter(estado = producto_habilitado).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_PRODUCTOS_DESHABILITADOS)

            productos = Producto.objects.filter(estado = producto_habilitado)

            dto_productos = []

            for x in range(productos.__len__()):
                if (productos[x].stock_deposito + productos[x].stock_local) <= (productos[x].stock_minimo + cantidad):
                    dto_producto = DTOProducto(productos[x].codigo,
                                               productos[x].nombre,
                                               productos[x].marca,
                                               productos[x].medida,
                                               productos[x].unidad_medida.nombre,
                                               productos[x].stock_local,
                                               productos[x].stock_deposito,
                                               productos[x].stock_minimo,
                                               productos[x].estado.nombre)
                    dto_productos.append(dto_producto)
            response.content = armar_response_list_content(dto_productos)
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
def obtener_reporte_compras_ventas(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if FECHA_DESDE in datos and not (FECHA_DESDE == ''):
                fecha_desde = datos[FECHA_DESDE]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_FECHA_DESDE_FALTANTE)

            if FECHA_HASTA in datos and not (FECHA_HASTA == ''):
                fecha_hasta = datos[FECHA_HASTA]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_FECHA_HASTA_FALTANTE)

            if datetime.datetime.strptime(fecha_desde, "%Y-%m-%d") > datetime.datetime.strptime(fecha_hasta,"%Y-%m-%d"):
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_FECHA_DESDE_MAYOR_HASTA)

            tipo_movimiento_compra = TipoMovimientoStock.objects.get(nombre = MOVIMIENTO_COMPRA)
            tipo_movimient_venta = TipoMovimientoStock.objects.get(nombre = MOVIMIENTO_VENTA)

            estado_creado = EstadoMovimientoStock.objects.get(nombre=ESTADO_CREADO)
            estado_pagado = EstadoMovimientoStock.objects.get(nombre=ESTADO_PAGADO)

            total_compras = 0.0
            total_ventas = 0.0

            if MovimientoStock.objects.filter(tipo_movimiento = tipo_movimiento_compra).__len__()>=1:
                compras = MovimientoStock.objects.filter( tipo_movimiento = tipo_movimiento_compra,
                                                          fecha_creacion__gte = fecha_desde,
                                                          fecha_creacion__lte = fecha_hasta)

                for x in range(0,compras.__len__()):
                    if (compras[x].estado == estado_creado or compras[x].estado == estado_pagado):
                        total_compras += compras[x].total_final

            if MovimientoStock.objects.filter(tipo_movimiento=tipo_movimient_venta).__len__() >= 1:
                ventas = MovimientoStock.objects.filter(tipo_movimiento=tipo_movimient_venta,
                                                        fecha_creacion__gte = fecha_desde,
                                                        fecha_creacion__lte = fecha_hasta)

                for x in range(0, ventas.__len__()):
                    if (ventas[x].estado == estado_creado or ventas[x].estado == estado_pagado):
                        total_ventas += ventas[x].total_final

            if total_compras == 0.0 and total_ventas == 0.0:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_COMPRAS_VENTAS_CERO)

            dto_reporte = DTOReporteComprasVentas(total_compras,total_ventas)

            response.content = armar_response_content(dto_reporte)
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
def obtener_reporte_ganancia_producto(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if FECHA_DESDE in datos and not (datos[FECHA_DESDE] == ''):
                fecha_desde = datos[FECHA_DESDE]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_FECHA_DESDE_FALTANTE)

            if FECHA_HASTA in datos and not (datos[FECHA_HASTA] == ''):
                fecha_hasta = datos[FECHA_HASTA]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_FECHA_HASTA_FALTANTE)

            if datetime.datetime.strptime(fecha_desde, "%Y-%m-%d") > datetime.datetime.strptime(fecha_hasta,"%Y-%m-%d"):
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_FECHA_DESDE_MAYOR_HASTA)

            tipo_movimient_venta = TipoMovimientoStock.objects.get(nombre = MOVIMIENTO_VENTA)

            estado_creado = EstadoMovimientoStock.objects.get(nombre=ESTADO_CREADO)
            estado_pagado = EstadoMovimientoStock.objects.get(nombre=ESTADO_PAGADO)

            lista_productos = []

            if MovimientoStock.objects.filter(tipo_movimiento=tipo_movimient_venta).__len__() >= 1:
                ventas = MovimientoStock.objects.filter(tipo_movimiento=tipo_movimient_venta,
                                                        fecha_creacion__gte = fecha_desde,
                                                        fecha_creacion__lte = fecha_hasta)

                for x in range(0, ventas.__len__()):
                    if (ventas[x].estado == estado_creado or ventas[x].estado == estado_pagado):

                        if MovimientoStockDetalle.objects.filter(movimiento_stock = ventas[x].codigo).__len__()<1:
                            raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_VENTA_SIN_DETALLE)

                        detalles_venta = MovimientoStockDetalle.objects.filter(movimiento_stock = ventas[x].codigo)

                        for y in range(0, detalles_venta.__len__()):
                            codigo_producto = detalles_venta[y].producto.codigo
                            nombre_producto = detalles_venta[y].producto.nombre
                            marca_producto = detalles_venta[y].producto.marca
                            medida_producto = detalles_venta[y].producto.medida
                            unidad_medida_producto = detalles_venta[y].producto.unidad_medida.nombre
                            ganancia = round((detalles_venta[y].precio_unitario - detalles_venta[y].precio_compra) * detalles_venta[y].cantidad,2)

                            if lista_productos.__len__() == 0:
                                ganancia_producto = GananciaProducto(codigo_producto,
                                                                     nombre_producto,
                                                                     marca_producto,
                                                                     medida_producto,
                                                                     unidad_medida_producto,
                                                                     ganancia)
                                lista_productos.append(ganancia_producto)
                            else:
                                for z in range(0,lista_productos.__len__()):
                                    if lista_productos[z].codigo == detalles_venta[y].producto.codigo:
                                        lista_productos[z].ganancia += ganancia
                                        break
                                    else:
                                        ganancia_producto = GananciaProducto(codigo_producto,
                                                                             nombre_producto,
                                                                             marca_producto,
                                                                             medida_producto,
                                                                             unidad_medida_producto,
                                                                             ganancia)
                                        lista_productos.append(ganancia_producto)
                                        break
            response.content = armar_response_list_content(lista_productos)
            response.status_code = 200
            return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)


class GananciaProducto:

    def __init__(self, codigo, nombre,marca,medida,unidad_medida, ganancia):
        self.codigo = codigo
        self.nombre = str(nombre),
        self.marca = marca,
        self.medida = medida,
        self.unidad_medida = unidad_medida
        self.ganancia = ganancia

    def as_json(self):
        return dict(
            codigo=self.codigo,
            nombre=self.nombre,
            marca=self.marca,
            medida=self.medida,
            unidad_medida=self.unidad_medida,
            ganancia= round(self.ganancia,2)
        )