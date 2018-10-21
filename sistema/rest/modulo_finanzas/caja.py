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
from sistema.utils.dto import  *
from sistema.utils.error_handler import *

@transaction.atomic()
@metodos_requeridos([METODO_POST])
def generar_detalle_caja(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if CODIGO in datos and not (CODIGO == ''):
                id_movimiento = datos[CODIGO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CODIGO_MOVIMIENTO_CAPITAL_FALTANTE)

            estado_movimiento_capital_pagado = EstadoMovimientoCapital.objects.get(nombre = ESTADO_PAGADO)

            if MovimientoCapital.objects.filter(codigo = id_movimiento, estado = estado_movimiento_capital_pagado).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_MOVIMIENTO_CAPITAL_INEXISTENTE)

            movimiento_capital = MovimientoCapital.objects.get(codigo = id_movimiento, estado = estado_movimiento_capital_pagado)

            #busco que exista una caja abierta

            estado_caja_abierta = EstadoCaja.objects.get(nombre = ESTADO_ABIERTA)

            if Caja.objects.filter(fecha_cierre = None, estado = estado_caja_abierta).__len__()<1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CAJA_CERRADA)

            caja = Caja.objects.get(fecha_cierre = None, estado = estado_caja_abierta)

            caja_detalle = CajaDetalle(total = movimiento_capital.total,
                                       fecha_creacion=datetime.datetime.now(pytz.utc),
                                       movimiento_capital = movimiento_capital,
                                       caja = caja)
            caja_detalle.save()
            response.content = armar_response_content(None, CREACION_DETALLE_CAJA)
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
def abrir_caja(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        # busco que exista una caja abierta

        estado_caja_abierta = EstadoCaja.objects.get(nombre=ESTADO_ABIERTA)

        if Caja.objects.filter(fecha_cierre=None, estado=estado_caja_abierta).__len__() >= 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CAJA_ABIERTA_EXISTENTE)
        else:
            ultima_caja = Caja.objects.order_by('codigo').last()
            if ultima_caja is None:
                total_apertura = 0
            else:
                total_apertura = ultima_caja.total_cierre

        caja = Caja(total_apertura = total_apertura,
                    fecha_apertura = datetime.datetime.now(pytz.utc),
                    estado = estado_caja_abierta
                    )
        caja.saveNewCaja()
        response.content = armar_response_content(None, APERTURA_CAJA)
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
def cerrar_caja(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        # busco que exista una caja abierta

        estado_caja_abierta = EstadoCaja.objects.get(nombre=ESTADO_ABIERTA)
        estado_caja_cerrada = EstadoCaja.objects.get(nombre=ESTADO_CERRADA)

        if Caja.objects.filter(fecha_cierre=None, estado=estado_caja_abierta).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CAJA_ABIERTA)
        else:
            caja = Caja.objects.get(fecha_cierre=None, estado=estado_caja_abierta)

            if CajaDetalle.objects.filter(caja = caja).__len__() <1:
                total_cierre = 0
            else:
                caja_detalles = CajaDetalle.objects.filter(caja = caja)
                total_cierre = caja.total_apertura

                for x in range(0, caja_detalles.__len__()):
                    if caja_detalles[x].movimiento_capital.estado.nombre == ESTADO_PAGADO:
                        if caja_detalles[x].movimiento_capital.tipo_movimiento.nombre == MOVIMIENTO_ENTRADA_CAPITAL:
                            total_cierre += caja_detalles[x].total
                        else:
                            total_cierre -= caja_detalles[x].total
            caja.estado = estado_caja_cerrada
            caja.fecha_cierre = datetime.datetime.now(pytz.utc)
            caja.total_cierre = total_cierre
            caja.save()
        response.content = armar_response_content(None, CIERRE_CAJA)
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
def obtener_ultima_caja(request):
    try:
        response = HttpResponse()

        if Caja.objects.all().__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_NO_HAY_CAJA)
        else:
            caja = Caja.objects.order_by('codigo').last()

        dto_caja_cabecera = DTOCajaCabecera(parsear_fecha_a_hora_arg(caja.fecha_apertura),
                                            parsear_fecha_a_hora_arg(caja.fecha_cierre),
                                            caja.total_apertura,
                                            caja.total_cierre,
                                            caja.estado.nombre)
        dto_list_caja_detalle = []
        if CajaDetalle.objects.filter(caja = caja).__len__()>=1:
            caja_detalles = CajaDetalle.objects.filter(caja = caja)
            for x in range(0, caja_detalles.__len__()):
                if(caja_detalles[x].movimiento_capital.estado.nombre == ESTADO_PAGADO):
                    dto_caja_detalle = DTOCajaDetalle(caja_detalles[x].fecha_creacion,
                                                      caja_detalles[x].total,
                                                      caja_detalles[x].movimiento_capital.tipo_movimiento.nombre,
                                                      caja_detalles[x].movimiento_capital.descripcion_movimiento
                                                     )
                    dto_list_caja_detalle.append(dto_caja_detalle)
            dto_caja = DTOCaja(dto_caja_cabecera,dto_list_caja_detalle)
        else:
            dto_caja = DTOCaja(dto_caja_cabecera,dto_list_caja_detalle)
        response.content = armar_response_content(dto_caja)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)