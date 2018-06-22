from json import loads, dumps

from django.core.serializers.json import DjangoJSONEncoder
from sistema.utils.constantes import *
from sistema.utils.error_handler import *


def obtener_datos_json(request):
    try:
        received_json_data = str(request.body)
        datos = loads(received_json_data)
        return datos
    except (KeyError, TypeError, ValueError, SystemError, RuntimeError):
        return ""

def armar_response_list_content(lista):
    response_dictionary = {}

    if lista is not None and not len(lista) == 0:

        try:
            response_dictionary[KEY_DATOS_OPERACION] = [item.as_json() for item in lista]
        except (KeyError, TypeError, ValueError, SystemError, RuntimeError):
            response_error_dictionary = {KEY_RESULTADO_OPERACION: False, KEY_DETALLE_OPERACION: DETALLE_ERROR_SISTEMA}
            return dumps(response_error_dictionary, cls=DjangoJSONEncoder)

    try:
        return dumps(response_dictionary, cls=DjangoJSONEncoder)
    except (KeyError, TypeError, ValueError, SystemError, RuntimeError):
        response_error_dictionary = {KEY_RESULTADO_OPERACION: False, KEY_DETALLE_OPERACION: DETALLE_ERROR_SISTEMA}
        return dumps(response_error_dictionary, cls=DjangoJSONEncoder)

