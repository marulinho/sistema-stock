# coding=utf-8
from json import dumps

from django.core.serializers.json import DjangoJSONEncoder

ERROR_METODO_INCORRECTO = 'ERROR_METODO_INCORRECTO'

ERROR_DATOS_INCORRECTOS = 'ERROR_DATOS_INCORRECTOS'
ERROR_DATOS_FALTANTES = 'ERROR_DATOS_FALTANTES'
DETALLE_ERROR_DATOS_INCOMPLETOS = "Faltan ingresar datos"

ERROR_DE_SISTEMA = 'ERROR_DE_SISTEMA'
DETALLE_ERROR_SISTEMA = "Error procesando llamada"


KEY_ERROR_CODE = 'error_code'
KEY_ERROR_DESCRIPTION = 'error_description'


# Metodos

def build_error(response, error_code, error_descripcion):
    content = {KEY_ERROR_DESCRIPTION: error_descripcion, KEY_ERROR_CODE: error_code}
    response.content = dumps(content, cls=DjangoJSONEncoder)

    return response


def build_bad_request_error(response, error_code, error_descripcion):
    response.status_code = 400
    return build_error(response, error_code, error_descripcion)


def build_unauthorized_error(response, error_code, error_descripcion):
    response.status_code = 401

    return build_error(response, error_code, error_descripcion)


def build_method_not_allowed_error(response, error_code, error_descripcion):
    response.status_code = 405

    return build_error(response, error_code, error_descripcion)


def build_internal_server_error(response, error_code, error_descripcion):
    response.status_code = 500

    return build_error(response, error_code, error_descripcion)
