# coding=utf-8
from json import dumps

from django.core.serializers.json import DjangoJSONEncoder

#Error llamada api call
ERROR_METODO_INCORRECTO = 'ERROR_METODO_INCORRECTO'

#Error datos incompletos al hacer el api call
ERROR_DATOS_INCORRECTOS = 'ERROR_DATOS_INCORRECTOS'
ERROR_DATOS_FALTANTES = 'ERROR_DATOS_FALTANTES'
DETALLE_ERROR_DATOS_INCOMPLETOS = "Faltan ingresar datos"

ERROR_DE_SISTEMA = 'Error de sistema'
DETALLE_ERROR_SISTEMA = "Error procesando llamada"

KEY_ERROR_CODE = 'error_code'
KEY_ERROR_DESCRIPTION = 'error_description'

#Error datos faltantes entidades
DETALLE_ERROR_REGISTRACION_USUARIO_FALTANTE = "Debe ingresar el usuario"
DETALLE_ERROR_REGISTRACION_CONTRASENIA_FALTANTE = "Debe ingresar la contraseña"
DETALLE_ERROR_REGISTRACION_NOMBRE_FALTANTE = "Debe ingresar el nombre del usuario"
DETALLE_ERROR_REGISTRACION_APELLIDO_FALTANTE = "Debe ingresar el apellido del usuario"
DETALLE_ERROR_REGISTRACION_PREGUNTA_FALTANTE = "Debe seleccionar una pregunta de seguridad"
DETALLE_ERROR_PREGUNTA_FALTANTE = "Debe ingresar el identificador de la pregunta de seguridad"
DETALLE_ERROR_PREGUNTA_INEXISTENTE = "No existe la pregunta de seguridad ingresada"
DETALLE_ERROR_RESPUESTAS_NO_COINCIDEN = "Las respuestas de seguridad no coinciden"
DETALLE_ERROR_REGISTRACION_PREGUNTA_NO_EXISTE = "Debe seleccionar una pregunta existente"
DETALLE_ERROR_REGISTRACION_USUARIO_EXISTE = "Usuario existente, intente con un nuevo usuario"
DETALLE_ERROR_REGISTRACION_USUARIO_INEXISTENTE = "No existe el usuario ingresado"
DETALLE_ERROR_REGISTRACION_USUARIO_CONTRASENIA_IGUALES = "Debe ingresar una contrasenia distinta al usuario"
DETALLE_ERROR_REGISTRACION_RESPUESTA_DESCRIPCION_FALTANTE = "Debe ingresar una respuesta"
DETALLE_ERROR_ID_USUARIO_FALTANTE = "Debe ingresar el identificador del usuario"
DETALLE_ERROR_CAMBIAR_CONTRASENIA_NUEVA_FALTANTE = "Debe ingresar una contrasenia nueva"
DETALLE_ERROR_CAMBIAR_CONTRASENIA_ACTUAL_FALTANTE = "Debe ingresar la contrasenia actual"
DETALLE_ERROR_CAMBIAR_CONTRASENIA_ACTUAL_NUEVA_IGUALES = "Las contrasenias deben ser diferentes"
DETALLE_ERROR_CREDENCIALES_INCORRECTAS = "Usuario o contraseña incorrecta"
DETALLE_ERROR_LOGOUT_SIN_LOGIN = "Debe iniciar sesion antes de cerrarla"
DETALLE_ERROR_LOGOUT_FALLIDO = "No se pudo cerra sesion, intente de nuevo"
DETALLE_ERROR_LOGOUT_EXITOSO = "Finalizo la sesion correctamente"

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
