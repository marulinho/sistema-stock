from __future__ import unicode_literals

import datetime
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
def generar_retiro_capital(request):
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

            usuario_ingresado = Usuario.objects.get(id = id_usuario)

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
                                                          descripcion_movimiento = '',
                                                          tipo_movimiento = salida_movimiento_capital,
                                                          estado = estado_movimiento_capital_pagado,
                                                          movimiento_stock = None,
                                                          usuario = usuario_ingresado,
                                                          forma_pago = forma_pago
                                                          )
            movimiento_capital_salida.saveNewMovimientoCapital()
            movimiento_capital_salida.descripcion_movimiento = (RETIRO_MOVIMIENTO_CAPITAL + str(movimiento_capital_salida.codigo) + ' ' + str(descripcion))
            movimiento_capital_salida.save()

            dto_movimiento_capital = DTOMovimientoCapital(movimiento_capital_salida.codigo,
                                                          movimiento_capital_salida.total,
                                                          movimiento_capital_salida.fecha_creacion,
                                                          movimiento_capital_salida.descripcion_movimiento,
                                                          movimiento_capital_salida.tipo_movimiento.nombre,
                                                          movimiento_capital_salida.estado.nombre,
                                                          movimiento_capital_salida.movimiento_stock,
                                                          movimiento_capital_salida.forma_pago.nombre,
                                                          movimiento_capital_salida.usuario.nombre)
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
@metodos_requeridos([METODO_PUT])
def cancelar_retiro_capital(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if CODIGO not in datos or CODIGO == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            id_movimiento_salida = datos[CODIGO]

            estado_movimiento_capital_pagado = EstadoMovimientoCapital.objects.get(nombre=ESTADO_PAGADO)

            if MovimientoCapital.objects.filter(codigo=id_movimiento_salida,
                                                estado=estado_movimiento_capital_pagado,
                                                movimiento_stock=None).__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_MOVIMIENTO_SALIDA_CAPITAL_INEXISTENTE)

            movimiento_capital = MovimientoCapital.objects.get(codigo=id_movimiento_salida, estado=estado_movimiento_capital_pagado, movimiento_stock = None)

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


@transaction.atomic()
@metodos_requeridos([METODO_GET])
def obtener_retiros(request):
    try:
        response = HttpResponse()

        if MovimientoCapital.objects.filter(movimiento_stock=None).__len__()<1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_RETIROS_INEXISTENTES)

        retiros = MovimientoCapital.objects.filter(movimiento_stock=None).order_by('-codigo')
        lista_retiros = []
        for x in range(0,retiros.__len__()):
            dto_retiro = DTOMovimientoCapital(retiros[x].codigo,
                                              retiros[x].total,
                                              retiros[x].fecha_creacion,
                                              retiros[x].descripcion_movimiento,
                                              retiros[x].tipo_movimiento.nombre,
                                              retiros[x].estado.nombre,
                                              retiros[x].movimiento_stock,
                                              retiros[x].forma_pago.nombre,
                                              retiros[x].usuario.nombre)
            lista_retiros.append(dto_retiro)

        response.content = armar_response_list_content(lista_retiros)
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
def obtener_retiro_id(request,id_retiro):
    try:
        response = HttpResponse()
        if id_retiro == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_CODIGO_RETIRO_FALTANTE)

        if MovimientoCapital.objects.filter(movimiento_stock=None, codigo = id_retiro).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_RETIROS_INEXISTENTES)

        retiro = MovimientoCapital.objects.get(movimiento_stock=None, codigo = id_retiro)

        dto_retiro = DTOMovimientoCapital(retiro.codigo,
                                          retiro.total,
                                          retiro.fecha_creacion,
                                          retiro.descripcion_movimiento,
                                          retiro.tipo_movimiento.nombre,
                                          retiro.estado.nombre,
                                          retiro.movimiento_stock,
                                          retiro.forma_pago.nombre,
                                          retiro.usuario.nombre)

        response.content = armar_response_content(dto_retiro)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)