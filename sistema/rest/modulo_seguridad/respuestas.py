from __future__ import unicode_literals

from django.db import transaction
from django.db import IntegrityError
from django.http import HttpResponse

from sistema.models import *
from sistema.utils.utils import *
from sistema.utils.constantes import *
from sistema.utils.decorators import *
from sistema.utils.error_handler import *

@transaction.atomic()
@metodos_requeridos([METODO_GET])
def obtener_respuesta_pregunta_usuario(request,id_usuario,id_pregunta):
    try:
        response = HttpResponse()
        if id_usuario == '' or id_usuario is None:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_ID_USUARIO_FALTANTE)
        if id_pregunta == '' or id_pregunta is None:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_PREGUNTA_FALTANTE)
        if Usuario.objects.get(id = id_usuario) is None:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_USUARIO_INEXISTENTE)
        if Pregunta.objects.get(id = id_pregunta) is None:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_REGISTRACION_USUARIO_INEXISTENTE)
        if RespuestaPregunta.objects.get(usuario = id_usuario , pregunta = id_pregunta) is None:
            raise ValueError(ERROR_DATOS_INCORRECTOS, DETALLE_ERROR_RESPUESTA_INEXISTENTE)
        respuesta = RespuestaPregunta.objects.get(usuario = id_usuario , pregunta = id_pregunta)
        response.content = armar_response_content(respuesta)
        response.status_code = 200
        return response
    except ValueError as err:
        print err.args
        return build_bad_request_error(response, err.args[0], err.args[1])

    except (IntegrityError, ValueError) as err:
        print err.args
        response.status_code = 401
        return build_bad_request_error(response, ERROR_DE_SISTEMA, DETALLE_ERROR_SISTEMA)
