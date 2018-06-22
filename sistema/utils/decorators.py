from functools import wraps

from django.http import HttpResponse
from sistema.utils.error_handler import *
from django.utils.decorators import available_attrs


def metodos_requeridos(request_method_list):
    """
    Controla si el metodo enviado es correcto
    :param request_method_list:
    :return:
    """
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            if request.method not in request_method_list:
                return build_method_not_allowed_error(HttpResponse(), ERROR_METODO_INCORRECTO,
                                                      'Metodo/s requeridos: ' + ', '.join(request_method_list))
            return func(request, *args, **kwargs)
        return inner
    return decorator