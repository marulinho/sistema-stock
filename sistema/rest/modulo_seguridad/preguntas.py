from __future__ import unicode_literals
from django.db import transaction
from django.db import IntegrityError
from django.http import HttpResponse

from sistema.models import Pregunta, Usuario
from sistema.utils.utils import *
from sistema.utils.constantes import *
from sistema.utils.decorators import *
from sistema.utils.error_handler import *

@transaction.atomic()
@metodos_requeridos([METODO_GET])
def buscar_preguntas(request):

    response = HttpResponse()

    try:
        preguntas = Pregunta.objects.filter(habilitado = True)
        response.content = armar_response_list_content(preguntas)
        response.status_code = 200
        return response

    except (IntegrityError, TypeError, KeyError):
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_GET])
def obtener_pregunta_id(request,id_pregunta):
    try:
        response = HttpResponse()
        if id_pregunta == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PREGUNTA_FALTANTE)
        else:
            if Pregunta.objects.get(id = id_pregunta):
                pregunta = Pregunta.objects.get(id = id_pregunta)
                response.content = armar_response_content(pregunta)
                response.status_code = 200
                return response
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PREGUNTA_INEXISTENTE)
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_POST])
def obtener_pregunta_descripcion(request):
    try:
        datos = obtener_datos_json(request)
        response = HttpResponse()

        if datos == {}:
            raise ValueError(ERROR_DATOS_FALTANTES, DETALLE_ERROR_DATOS_INCOMPLETOS)
        else:
            if PREGUNTA_DESCRIPCION in datos and not (PREGUNTA_DESCRIPCION ==''):
                pregunta = Pregunta.objects.get(descripcion = datos[PREGUNTA_DESCRIPCION])
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_DESCRIPCION_PREGUNTA_FALTANTE)
            if pregunta:
                response.content = armar_response_content(pregunta)
                response.status_code = 200
                return response
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PREGUNTA_INEXISTENTE)
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)

@transaction.atomic()
@metodos_requeridos([METODO_GET])
def obtener_pregunta_usuario(request,usuario):
    try:
        response = HttpResponse()
        if usuario == '':
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_ID_USUARIO_FALTANTE)
        else:
            if Usuario.objects.get(usuario = usuario):
                usuario_pregunta = Usuario.objects.get(usuario = usuario).pregunta_id
                if Pregunta.objects.get(id=usuario_pregunta) is None:
                    raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PREGUNTA_INEXISTENTE)
                else:
                    pregunta = Pregunta.objects.get(id=usuario_pregunta)
                    response.content = armar_response_content(pregunta)
                    response.status_code = 200
                    return response
            else:
                raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_USUARIO_INEXISTENTE)
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)
