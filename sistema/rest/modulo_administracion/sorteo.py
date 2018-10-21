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
def registrar_sorteo(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if NOMBRE in datos and not (NOMBRE == ''):
                nombre = datos[NOMBRE]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_NOMBRE_FALTANTE)

            sorteo_habilitado = EstadoSorteo.objects.get(nombre = ESTADO_HABILITADO)

            if Sorteo.objects.filter(nombre = nombre, estado = sorteo_habilitado).__len__()>=1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_NOMBRE_SORTEO_EXISTENTE)

            if LISTA_SORTEO in datos and not (datos[LISTA_SORTEO] == []):
                lista_sorteo= datos[LISTA_SORTEO]
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_LISTA_SORTEO_FALTANTE)

            producto_habilitado = EstadoProducto.objects.get(nombre = ESTADO_HABILITADO)

            sorteo_creado = Sorteo(nombre = nombre,
                                   estado = sorteo_habilitado,
                                   fecha_creacion=datetime.datetime.now(pytz.utc))

            sorteo_creado.saveNewSorteo()

            for x in range(lista_sorteo.__len__()):
                if Producto.objects.filter(codigo = lista_sorteo[x]['producto'], estado = producto_habilitado).__len__()<1:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PRODUCTO_INEXISTENTE)

                producto = Producto.objects.get(codigo = lista_sorteo[x]['producto'], estado = producto_habilitado)

                if producto.stock_local < lista_sorteo[x]['cantidad']:
                    if producto.stock_deposito < lista_sorteo[x]['cantidad']:
                        raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_CANTIDAD_SORTEO_MAYOR)
                    else:
                        producto.stock_deposito -= lista_sorteo[x]['cantidad']
                else:
                    producto.stock_local -= lista_sorteo[x]['cantidad']
                producto.save()

                detalle_sorteo = SorteoDetalle(producto = producto,
                                               cantidad = lista_sorteo[x]['cantidad'],
                                               posicion = lista_sorteo[x]['posicion'],
                                               ganador = lista_sorteo[x]['ganador'],
                                               sorteo = sorteo_creado)
                detalle_sorteo.save()

            dto_sorteo = DTOSorteoCabecera(sorteo_creado.codigo,
                                           sorteo_creado.nombre,
                                           sorteo_creado.estado.nombre,
                                           sorteo_creado.fecha_creacion)
            response.content = armar_response_content(dto_sorteo)
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
def obtener_sorteos(request):
    try:
        response = HttpResponse()

        sorteo_habilitado = EstadoSorteo.objects.get(nombre = ESTADO_HABILITADO)

        if Sorteo.objects.filter(estado = sorteo_habilitado).__len__()<1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_SORTEOS_INEXISTENTES)

        sorteos = Sorteo.objects.filter(estado = sorteo_habilitado).order_by('-codigo')
        listas_sorteos = []
        for x in range(0,sorteos.__len__()):
            dto_sorteo = DTOSorteoCabecera(sorteos[x].codigo,
                                            sorteos[x].nombre,
                                            sorteos[x].estado.nombre,
                                            sorteos[x].fecha_creacion)
            listas_sorteos.append(dto_sorteo)

        response.content = armar_response_list_content(listas_sorteos)
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
def obtener_sorteo_id(request,id_sorteo):
    try:
        response = HttpResponse()
        if id_sorteo == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS,DETALLE_ERROR_CODIGO_SORTEO_FALTANTE)

        sorteo_habilitado = EstadoSorteo.objects.get(nombre = ESTADO_HABILITADO)

        if Sorteo.objects.filter(codigo = id_sorteo, estado=sorteo_habilitado).__len__() < 1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_SORTEO_INEXISTENTE)

        sorteo =  Sorteo.objects.get(codigo = id_sorteo, estado=sorteo_habilitado)

        if SorteoDetalle.objects.filter(sorteo = sorteo).__len__()<1:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_SORTEO_SIN_DETALLE)

        detalles_sorteo = SorteoDetalle.objects.filter(sorteo = sorteo)

        dto_detalles_sorteo = []
        dto_cabecera_sorteo = DTOSorteoCabecera(sorteo.codigo,
                                                sorteo.nombre,
                                                sorteo.estado.nombre,
                                                sorteo.fecha_creacion)
        for x in range(detalles_sorteo.__len__()):

            if Producto.objects.filter(codigo=detalles_sorteo[x].producto.codigo).__len__() < 1:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PRODUCTO_INEXISTENTE)

            producto = Producto.objects.get(codigo=detalles_sorteo[x].producto.codigo)

            dto_detalle_sorteo = DTOSorteoDetalle(producto.codigo,
                                                  str(producto.nombre) +' - '+str(producto.marca) +' - '+str(producto.medida) +' '+str(producto.unidad_medida.nombre),
                                                  detalles_sorteo[x].cantidad,
                                                  detalles_sorteo[x].posicion,
                                                  detalles_sorteo[x].ganador)

            dto_detalles_sorteo.append(dto_detalle_sorteo)
        dto_sorteo = DTOSorteo(dto_cabecera_sorteo,dto_detalles_sorteo)
        response.content = armar_response_content(dto_sorteo)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)