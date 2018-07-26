from __future__ import unicode_literals

from string import lower
from django.db import transaction
from django.db import IntegrityError

from sistema.models import *
from sistema.utils.utils import *
from sistema.utils.constantes import *
from sistema.utils.decorators import *
from sistema.utils.error_handler import *

@transaction.atomic()
@metodos_requeridos([METODO_GET])
def obtener_unidad_medida(request):

    try:
        response = HttpResponse()
        estado_habilitado = EstadoUnidadMedida.objects.get(nombre=ESTADO_HABILITADO)
        if UnidadMedida.objects.filter(estado = estado_habilitado).__len__()<1:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_UNIDAD_MEDIDA_HABILITADA)
        else:
            unidades_medida = UnidadMedida.objects.filter(estado = estado_habilitado)
            response.content = armar_response_list_content(unidades_medida)
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
def obtener_unidad_medida_id(request,id_unidad_medida):

    try:
        response = HttpResponse()
        if id_unidad_medida == '':
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_ID_UNIDAD_MEDIDA_FALTANTE)
        estado_habilitado = EstadoUnidadMedida.objects.get(nombre=ESTADO_HABILITADO)
        if UnidadMedida.objects.filter(id = id_unidad_medida,
                                       estado = estado_habilitado).__len__()<1:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_ID_UNIDAD_MEDIDA_INEXISTENTE)
        else:
            unidad_medida = UnidadMedida.objects.get(id = id_unidad_medida,
                                                        estado = estado_habilitado)
            response.content = armar_response_content(unidad_medida)
            response.status_code = 200
            return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

